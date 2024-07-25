from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)


def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List[Dict], bool]:
    tape = list(input_)
    head_position = 0
    current_state = machine['start state']
    blank_symbol = machine['blank']
    final_states = set(machine['final states'])
    transition_table = machine['table']
    history = []
    step_count = 0

    while steps is None or step_count < steps:
        if head_position < 0:
            tape.insert(0, blank_symbol)
            head_position = 0
        elif head_position >= len(tape):
            tape.append(blank_symbol)
        
        current_symbol = tape[head_position]
        state_transitions = transition_table.get(current_state, {})

        if current_symbol not in state_transitions:
            return ''.join(tape).strip(blank_symbol), history, current_state in final_states

        transition = state_transitions[current_symbol]

        history.append({
            'state': current_state,
            'reading': current_symbol,
            'position': head_position,
            'memory': ''.join(tape),
            'transition': transition
        })

        if isinstance(transition, str):
            if transition == 'R':
                head_position += 1
            elif transition == 'L':
                head_position -= 1
            else:
                raise ValueError(f"Invalid transition direction: {transition}")
        else:
            if 'write' in transition:
                tape[head_position] = transition['write']
            if 'R' in transition:
                current_state = transition['R']
                head_position += 1
            elif 'L' in transition:
                current_state = transition['L']
                head_position -= 1
        
        step_count += 1

    return ''.join(tape).strip(blank_symbol), history, current_state in final_states
