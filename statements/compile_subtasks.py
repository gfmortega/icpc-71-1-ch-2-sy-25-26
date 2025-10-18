#!/usr/bin/env python3.8
from functools import partial
from glob import glob
from os import sep
import re



old_subtask_head = re.compile(r'^\\textbf{Subtask (?P<subtask_id>\d+)} \((?P<points>\d+) points?\):?(?P<inline_part>.*)$')
new_subtask_open = re.compile(r'^\s*\\subtask{(?P<subtask_id>\d+)}{(?P<points>\d+)}{(?P<inline_part>.*}?)$')
new_subtask_close = re.compile(r'^\s*}\s*$')
for_all_subtasks = re.compile(r'^\\textbf{For all subtasks}.*$')
subtask_usage = '% Usage: \\subtask{SUBTASK_ID}{POINTS}{CONSTRAINTS}'
cf_header = [
    "BEGIN POLYGON/CODEFORCES VERSION.",
    "",
    "This is what you should use for Polygon/CF.",
    "This is automatically generated based on the subtask list above.",
    "Please don't edit this section directly; It will be overwritten.",
    "Instead, edit the subtask list above and then run `./compile_subtasks.py'.",
    "(needs python3.8)",
    "Commit your edits first before running this!",
]
cf_footer = [
    "END POLYGON/CODEFORCES VERSION.",
]
cf_max_length = max(len(line) for cf_box in (cf_header, cf_footer) for line in cf_box)
comment_cf_version_begin = '\\begin{comment} % CF Version'
comment_cf_version_end = '\\end{comment}'



def print_box(contents, file):
    print(file=file)
    print('%'*(cf_max_length + 4), file=file)
    for line in contents: print('%', line.ljust(cf_max_length), '%', file=file)
    print('%'*(cf_max_length + 4), file=file)
    print(file=file)



def remove_cf_version_comment_blocks(lines):
    writing = True
    for line in lines:
        if line.strip().startswith(comment_cf_version_begin):
            writing = False

        if writing:
            yield line

        if line.strip().endswith(comment_cf_version_end):
            writing = True

    assert writing



def parse_statement_subtasks(lines):
    r"""
    CF format:

    1 & \mathbf{11} & \begin{array}{l}
        \text{$1 \le n, m, N, M \le 10^3$} \\
        \text{$1 \le s_i \le t_i \le 10^3$}
    \end{array}
    \\ \hline



    Our format:

    \begin{subtasks}

        \subtask{1}{15}{
            $1 \le n, m, N, M \le 10^3$  \\
            $1 \le s_i \le t_i \le 10^3$
        }

    \end{subtasks}
    """

    lines = [*lines]

    # find constraints/scoring section
    section_groups = [[
        "Constraints",
        "Subtasks and Constraints",
        "Constraints and Subtasks",
    ], [
        "Scoring",
    ]]
    for section_group in section_groups:
        group = {f'\\subsection*{{{section}}}' for section in section_group}
        if res := [i for i, line in enumerate(lines) if line.strip() in group]:
            [i] = res
            break
    else:
        raise Exception
    j = next(j for j, line in enumerate(lines) if j > i and line.startswith('\\subsection*{'))

    pre, lines, post = lines[:i+1], lines[i+1:j], lines[j:]

    # remove comment blocks
    lines = [*remove_cf_version_comment_blocks(lines)]

    # find the list of subtask constraints
    pre_subtasks = []
    subtasks = []
    post_subtasks = []

    has_old_subtasks_format = any(old_subtask_head.match(line) for line in lines)
    has_new_subtasks_format = any('\\begin{subtasks}' in line for line in lines)

    def add_constraint_line(line):
        if line := line.strip():
            if line.startswith('%'):
                post_subtasks.append(line)
            else:
                subtasks[-1]['constraints'].append(line)

    assert not (has_old_subtasks_format and has_new_subtasks_format)
    if has_old_subtasks_format:
        # parse old format subtasks
        writing_pre = True
        for line in lines:
            if match := old_subtask_head.match(line):
                writing_pre = False
                subtasks.append({
                        'subtask_id': match.group('subtask_id'),
                        'points': match.group('points'),
                        'constraints': []
                    })

                add_constraint_line(match.group('inline_part'))
            elif writing_pre:
                pre_subtasks.append(line)
            else:
                add_constraint_line(line)

        assert not writing_pre
    elif has_new_subtasks_format:
        # parse new format subtasks
        i = next(i for i, line in enumerate(lines) if '\\begin{subtasks}' == line.strip())
        j = next(j for j, line in enumerate(lines) if '\\end{subtasks}' == line.strip())
        assert 0 <= i < j < len(lines)

        pre_subtasks = lines[:i]
        post_subtasks = lines[j+1:]

        writing_subtask = False
        for line in lines[i+1:j]:
            line = line.strip()
            if match := new_subtask_open.match(line):
                assert not writing_subtask
                writing_subtask = True
                subtasks.append({
                        'subtask_id': match.group('subtask_id'),
                        'points': match.group('points'),
                        'constraints': []
                    })

                if line := match.group('inline_part'):
                    assert line.endswith('}')
                    add_constraint_line(line[:-1])
                    writing_subtask = False

            elif new_subtask_close.match(line):
                assert writing_subtask
                writing_subtask = False
            elif writing_subtask:
                add_constraint_line(line)
            elif line.startswith('%'):
                post_subtasks.append(line) # skip comment
            else:
                assert not line # nothing outside of \subtask allowed!

        assert not writing_subtask


    else:
        # no subtasks
        pre_subtasks = lines

    # remove blank lines
    pre_subtasks = [line for line in pre_subtasks if line.strip()]
    post_subtasks = [line for line in post_subtasks if line.strip()]

    # remove hint on \subtask usage
    pre_subtasks = [line for line in pre_subtasks if line.strip() != subtask_usage]

    # remove blanks at the end
    while post and not post[-1].strip(): post.pop()

    # try extracting the constraints from pre_subtasks
    if any('\\constraints{' in line for line in pre_subtasks):
        i, = (i for i, line in enumerate(pre_subtasks) if '\\constraints{' in line)
        j = next(j for j, line in enumerate(pre_subtasks) if line.strip() == '}' and j > i)
        pre_subtasks, constraints, mid_subtasks = pre_subtasks[:i], pre_subtasks[i+1:j], pre_subtasks[j+1:]
    elif any('\\textbf{For all subtasks}' in line for line in pre_subtasks):
        i, = (i for i, line in enumerate(pre_subtasks) if '\\textbf{For all subtasks}' in line)
        pre_subtasks, constraints, mid_subtasks = pre_subtasks[:i], pre_subtasks[i+1:], []
    else:
        pre_subtasks, constraints, mid_subtasks = [], pre_subtasks, []

    # remove \\ in constraints
    def cleanup(line):
        return line.rstrip('\\') if line.endswith('\\\\') else line
    constraints = [cleanup(line) for line in constraints]

    # take out the comments
    def take_out_comments(lines, mid_subtasks):
        constraints = []
        for line in lines:
            if line.strip():
                (mid_subtasks if line.strip().startswith('%') else constraints).append(line)

        return constraints
    constraints = take_out_comments(constraints, mid_subtasks)


    # replace label
    if subtasks and pre and pre[-1].strip() == '\\subsection*{Constraints}':
        pre[-1] = '\\subsection*{Constraints and Subtasks}'


    return pre, pre_subtasks, constraints, mid_subtasks, subtasks, post_subtasks, post



def write_constraints_our_version(constraints, file, *, header='constraints', indent=0, inline_one=False):
    if inline_one and len(constraints) == 1:
        [constraint] = constraints
        print(' '*indent, f'\\{header}{{{constraint}}}', sep='', file=file)
    elif len(constraints) > 0:
        print(' '*indent, f'\\{header}{{', sep='', file=file)
        for index, constraint in enumerate(constraints):
            constraint = constraint.strip()
            if index != len(constraints) - 1 and not constraint.endswith('\\\\'):
                constraint += '  \\\\'
            print(' '*indent, f'    {constraint}', sep='', file=file)
        print(' '*indent, '}', sep='', file=file)
    print(file=file)



def write_constraints_cf_old_version(constraints, file, *, has_header=True):
    if constraints and has_header:
        print('\\textbf{For all subtasks}', file=file)

    for constraint in constraints:
        constraint = constraint.strip()
        if constraint.endswith('\\\\'):
            constraint = constraint.rstrip('\\').rstrip()
        constraint = ' '.join(re.split(r' \\\\ ', constraint))
        print(file=file)
        print(constraint, file=file)
    print(file=file)
    print(file=file)



def write_constraints_section_our_version(pre_subtasks, constraints, mid_subtasks, subtasks, post_subtasks, has_long, file):
    # write pre-subtasks lines
    for line in pre_subtasks:
        print(line.rstrip('\n'), file=file)
        print(file=file)
    print(file=file)

    # write global constraints  
    if subtasks:
        write_constraints_our_version(constraints, file)
    else:
        write_constraints_cf_old_version(constraints, file, has_header=False)

    # write mid-subtasks lines
    for line in mid_subtasks:
        print(line.rstrip('\n'), file=file)
        print(file=file)
    print(file=file)

    # write subtasks
    if subtasks:
        print(subtask_usage, file=file)
        print('\\begin{subtasks}', file=file)
        print(file=file)

        for subtask in subtasks:
            subtask_id = subtask['subtask_id']
            points = subtask['points']
            constraints = subtask['constraints']
            header = f'subtask{{{subtask_id}}}{{{points}}}'
            assert constraints
            write_constraints_our_version(constraints, file=file, header=header, indent=4, inline_one=not has_long)

        print('\\end{subtasks}', file=file)
        print(file=file)
        print(file=file)


    # write post-subtasks lines
    for line in post_subtasks:
        print(line.rstrip('\n'), file=file)
        print(file=file)
    print(file=file)



def write_constraints_section_cf_version(pre_subtasks, constraints, mid_subtasks, subtasks, post_subtasks, has_long, file):
    print("CF subtasks!!!!", subtasks)
    if True:

        # write header
        print(file=file)
        print(file=file)
        print(comment_cf_version_begin, file=file)
        print(file=file)
        print_box(cf_header, file=file)
        print(file=file)

        # write pre-subtasks lines
        for line in pre_subtasks:
            print(line.rstrip('\n'), file=file)
            print(file=file)
        print(file=file)

        def open_math():
            if constraints or subtasks:
                print("$$\\begin{align*}", file=file)
                print(file=file)

        def close_math():
            if constraints or subtasks:
                print("\\end{align*}$$", file=file)
                print(file=file)

        def textify(constraint, joiner=r' \\ '):
            constraint = constraint.strip()
            if constraint.endswith('\\\\'):
                constraint = constraint.rstrip('\\').rstrip()

            if constraint.startswith('$') and constraint.endswith('$') and '$' not in constraint[1:-1]:
                return constraint[1:-1].strip()
            else:
                for tp in 'bf', 'it', 'tt':
                    constraint = re.sub(rf'\\text{tp}\s*\{{([^\}}]+)\}}', rf'}}\\math{tp}{{\1}}\\text{{', constraint)
                return joiner.join(f"\\text{{{constraint_piece}}}" for constraint_piece in constraint.split(r' \\ '))

        subtask_textify = partial(textify, joiner=r' \\ && ')
        open_math()

        # write global constraints
        if constraints:
            print("&\\begin{array}{|l|}", file=file)
            print("    \\hline", file=file)
            print("    \\text{Constraints For All Subtasks}", file=file)
            print("    \\\\ \\hline", file=file)

            for constraint in constraints:
                print(f'    {textify(constraint)} \\\\', file=file)
            print(f'    \\hline', file=file)
            print('\\end{array}\\\\', file=file)
            print(file=file)

        # write mid-subtasks lines
        if mid_subtasks:
            close_math()
            for line in mid_subtasks:
                print(line.rstrip('\n'), file=file)
                print(file=file)
            print(file=file)
            open_math()

        # write subtasks
        if subtasks:
            print("&\\begin{array}{|c|c|l|}", file=file)
            print("    \\hline", file=file)
            print("    \\text{Subtask} & \\text{Points} & \\text{Constraints} \\\\ \\hline", file=file)
            if has_long: print(file=file)

            for subtask in subtasks:
                subtask_id = subtask['subtask_id']
                points = int(subtask['points'])
                constraint, *rest_constraints = subtask['constraints']

                assert points >= 1

                if has_long:
                    print(f'    {subtask_id} & \\mathbf{{{points}}} & {subtask_textify(constraint)} \\\\', file=file)
                    for constraint in rest_constraints:
                        print(f'    && {subtask_textify(constraint)} \\\\', file=file)
                    print(f'    \\hline', file=file)
                    print(file=file)
                else:
                    assert not rest_constraints
                    print(f'    {subtask_id} & \\mathbf{{{points}}} & {subtask_textify(constraint)} \\\\ \\hline', file=file)

            print('\\end{array}\\\\', file=file)
            print(file=file)

        close_math()

        # write post-subtasks lines
        for line in post_subtasks:
            print(line.rstrip('\n'), file=file)
            print(file=file)
        print(file=file)


        # write footer
        print_box(cf_footer, file=file)
        print(file=file)
        print(comment_cf_version_end, file=file)

        print(file=file)
        print(file=file)
        print(file=file)



def process_file(filename):
    print('checking filename', filename, end='...')

    # parse the file
    with open(filename) as file:
        pre, pre_subtasks, constraints, mid_subtasks, subtasks, post_subtasks, post = parse_statement_subtasks(line.rstrip('\n') for line in file.readlines())

    print('got', len(constraints), 'constraints and', len(subtasks), 'subtasks. ', end='')

    # time to write
    print('writing now...')
    with open(filename, 'w') as file:
        # write pre lines
        for line in pre:
            print(line.rstrip('\n'), file=file)
        print(file=file)

        has_long = any(len(subtask['constraints']) > 1 for subtask in subtasks)

        # print subtasks in the new format
        write_constraints_section_our_version(pre_subtasks, constraints, mid_subtasks, subtasks, post_subtasks, has_long, file=file)

        # write CF version of the subtasks
        write_constraints_section_cf_version(pre_subtasks, constraints, mid_subtasks, subtasks, post_subtasks, has_long, file=file)

        # separate from the rest of the lines
        print(file=file)

        # print post lines
        for line in post:
            print(line.rstrip('\n'), file=file)
        print(file=file)


if __name__ == '__main__':
    for filename in sorted((*glob(f'problems{sep}reservoir-doggos.tex'), *glob(f'elims{sep}*.tex'), *glob(f'finalspractice{sep}*.tex'), *glob(f'sparring{sep}*.tex'), *glob(f'statements{sep}*.tex'))):
        try:
            process_file(filename)
        except Exception as e:
            print(filename)
            print(e)
    print('done!')
