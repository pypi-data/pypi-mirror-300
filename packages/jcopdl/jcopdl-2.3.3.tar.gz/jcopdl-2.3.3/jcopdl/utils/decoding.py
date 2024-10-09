import torch
import numpy as np
import pandas as pd


def beam_search(model, init_sequence, stop_id, top_k=5, temp=1, alpha=0, max_length=50, multinomial=False, trim_stop_token=True):
    """
    Beam Search implementation to find a heuristic solution for next sequence prediction

    == input ==
    model: PyTorch Model
        should have .predict() method that returns probabilities and indexes from given logits. For example:
        def predict(self, x, k, temp=1, multinomial=False):
            x, _ = self.forward(x)
            if multinomial:
                return multinomial_sampling_from_logits(x, k, temp)
            else:
                return greedy_sampling_from_logits(x, k, temp)
                
    init_sequence: list[int]
        a list of ID as the initial sequence

    stop_id: int
        id for stopping criterion before the max_length is reached

    top_k: int
        beam width / beam size

    temp: float
        temperature of the softmax function.
        - Higher temperature results in a more uniform distribution
        - Lower temperature may highlight / sharpen the original distribution

    alpha: non negative float
        length normalization parameter
        - 0 means no normalization, would benefit short sentences
        - 1 means divided by length of sequence, fair for both short and long sentences
        - commonly used alpha is around 0.6 - 0.8

    max_length: int
        maximum sequence length as the stopping criterion

    multinomial: bool
        either to perform greedy topK sampling or multinomial sampling
        - True means to use multinomial sampling
        - False means to use greedy sampling
    """
    candidates = [(init_sequence, [1])]

    for _ in range(max_length):
        new_candidates = []
        for sequence, score in candidates:
            if sequence[-1] == stop_id:
                new_candidates.append((sequence, score))
            else:
                x = torch.LongTensor([sequence])
                probs, indexes = model.predict(x, top_k, temp, multinomial)
                for prob, idx in zip(probs[0], indexes[0]):
                    new_candidates.append((sequence + [idx.item()], score + [prob.item()]))
        
        # Sort and Update Candidates
        new_candidates.sort(key=lambda x: np.log(x[1]).sum() / len(x[0]) ** alpha, reverse=True)
        candidates = new_candidates[:top_k]

        # Stopping Criteria
        if all(sequence[-1] == stop_id for sequence, score in candidates):
            break

    best_sequence, best_score = max(candidates, key=lambda x: np.log(x[1]).sum() / len(x[0]) ** alpha)
    if (best_sequence[-1] == stop_id) and trim_stop_token:
        best_sequence = best_sequence[:-1]
    return best_sequence, best_score


def greedy_search(model, init_sequence, stop_id, temp=1, alpha=0, max_length=50, multinomial=False):
    return beam_search(model, init_sequence, stop_id, top_k=1, temp=temp, alpha=alpha, max_length=max_length, multinomial=multinomial)


def beam_search_with_steps(model, init_sequence, stop_id, top_k=1, show_top_k=5, temp=1, alpha=0, max_length=50, multinomial=False, trim_stop_token=True, lookup_token_func=None, lookup_tokens_func=None, prob_precision=None):
    """
    Beam Search implementation to find a heuristic solution for next sequence prediction

    == input ==
    model: PyTorch Model
        should have .predict() method that returns probabilities and indexes from given logits. For example:
        def predict(self, x, k, temp=1, multinomial=False):
            x, _ = self.forward(x)
            if multinomial:
                return multinomial_sampling_from_logits(x, k, temp)
            else:
                return greedy_sampling_from_logits(x, k, temp)
                
    init_sequence: list[int]
        a list of ID as the initial sequence

    stop_id: int
        id for stopping criterion before the max_length is reached

    top_k: int
        beam width / beam size

    show_top_k: int
        how many softmax result to show

    temp: float
        temperature of the softmax function.
        - Higher temperature results in a more uniform distribution
        - Lower temperature may highlight / sharpen the original distribution

    alpha: non negative float
        length normalization parameter
        - 0 means no normalization, would benefit short sentences
        - 1 means divided by length of sequence, fair for both short and long sentences
        - commonly used alpha is around 0.6 - 0.8

    max_length: int
        maximum sequence length as the stopping criterion

    multinomial: bool
        either to perform greedy topK sampling or multinomial sampling
        - True means to use multinomial sampling
        - False means to use greedy sampling
    """
    if show_top_k < top_k:
        show_top_k = top_k
    candidates = [(init_sequence, [1])]
    steps = []
    for _ in range(max_length):
        new_candidates = []
        trace = []
        for sequence, score in candidates:
            if sequence[-1] == stop_id:
                new_candidates.append((sequence, score))
            else:
                x = torch.LongTensor([sequence])
                probs, indexes = model.predict(x, show_top_k, temp, multinomial)
                for prob, idx in zip(probs[0], indexes[0]):
                    new_candidates.append((sequence + [idx.item()], score + [prob.item()]))    
                    if len(new_candidates) == top_k:
                        break

                df_trace = pd.DataFrame({
                    "candidate": indexes[0].tolist(),
                    "probability": probs[0].tolist()
                })
                df_trace["score"] = df_trace.probability.apply(lambda x: 100 + np.log(score).sum() + np.log(x))
                trace.append(df_trace)

        # Sort and Update Candidates. Also save candidates Traces
        new_candidates.sort(key=lambda x: np.log(x[1]).sum() / len(x[0]) ** alpha, reverse=True)
        candidates = new_candidates[:top_k]
        steps.append({
            "candidates": [candidate[0] for candidate in candidates],
            "trace": trace
        })

        # Stopping Criteria
        if all(sequence[-1] == stop_id for sequence, score in candidates):
            break        

    best_sequence, best_score = max(candidates, key=lambda x: np.log(x[1]).sum() / len(x[0]) ** alpha)
    if (best_sequence[-1] == stop_id) and trim_stop_token:
        best_sequence = best_sequence[:-1]
    for step in steps:
        for df in step["trace"]:
            if lookup_token_func:
                df.candidate = df.candidate.transform(lookup_token_func)
            if prob_precision:
                df.probability = df.probability.round(prob_precision)

        if lookup_tokens_func:
            step["candidates"] = [" ".join(lookup_tokens_func(candidate)) for candidate in step["candidates"]]

    if top_k == 1:
        steps = {
            "candidate": steps[-1]["candidates"][0],
            "trace": [trace for step in steps for trace in step["trace"]]
        }
    steps = __convert_steps_to_html(steps)
    return best_sequence, best_score, steps

def __convert_steps_to_html(steps):
    from html import escape as html_escape
    from IPython.core.display import HTML
    display_html = []
    if isinstance(steps, list):
        for step in steps:
            candidate_html = "<br>".join([f'Beam {i:02}: {html_escape(candidate)}' for i, candidate in enumerate(step["candidates"], 1)])
            trace_html = "".join([f'<div>{df._repr_html_()}</div>' for df in step["trace"]])
            display_html.append(f"""<div>{candidate_html}</div><div style="display:flex; gap: 50px; justify-content: left;">{trace_html}</div><hr>""")
    elif isinstance(steps, dict):
        candidate_html = f"""Best Candidate: {html_escape(steps["candidate"])}"""
        trace_html = "".join([f'<div>{df._repr_html_()}</div>' for df in steps["trace"]])
        display_html.append(f"""<div>{candidate_html}</div><div style="display:flex; gap: 50px; justify-content: left;">{trace_html}</div><hr>""")        
    return HTML("".join(display_html))
