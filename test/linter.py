import regex
import os

import cpplint

folder = "/home/pariterre/Programmation/biorbd"
folders_to_lint = [os.path.join(folder, 'src'), os.path.join(folder, 'binding')]

total_non_corrected_lines = 0
n_files = 0
for root, dirs, files in os.walk(folder):
    for file in files:
        is_file_in = False
        for folder_to_lint in folders_to_lint:
            if folder_to_lint in root:
                is_file_in = True
                break

        if not is_file_in or not file.endswith(".cpp"):
            continue
        filename = cpplint.ParseArguments([("--output=junit"), os.path.join(root, file)])[0]
        print("Checking: " + filename)

        # Process File
        with open(filename, 'r') as f:  # Read the non lint file
            lines = f.read()
        lines = lines.split("\n")

        changes_were_made = True
        non_corrected_lines = list()
        # Redo the lint until no automatic changes were made (changes may create new problems)
        while changes_were_made:
            changes_were_made = False
            non_corrected_lines.clear()

            # Process the file using the previous lines
            cpplint._cpplint_state = cpplint._CppLintState()
            cpplint.ParseArguments([("--output=junit"), filename])
            cpplint.ProcessFileData(filename, "cpp", lines, cpplint.Error, None)

            # Propose some easy to perform corrections
            if len(cpplint._cpplint_state._junit_failures) > 0:
                # Correct the required things
                cpplint._cpplint_state._junit_failures.reverse()  # Begin at the end
                for fail in cpplint._cpplint_state._junit_failures:
                    if fail[1] is None:
                        if 'should include its header file' in fail[2]:
                            pass
                        else:
                            non_corrected_lines.append(fail)
                        continue

                    lineno = fail[1] - 1  # 1 based

                    if regex.search('^Small and focused functions are preferred.*$', fail[2]):
                        pass

                    elif regex.search('^No copyright message found.*$', fail[2]):
                        pass

                    elif fail[2] == 'Lines should be <= 80 characters long':
                        non_corrected_lines.append(fail)

                    elif fail[2] == 'Include the directory when naming .h files':
                        # Ignore this one
                        pass

                    elif fail[2] == 'Tab found; better to use spaces':
                        lines[lineno] = lines[lineno].replace('\t', '    ')
                        changes_were_made = True

                    elif fail[2] == 'Redundant blank line at the start of a code block should be deleted.':
                        if lines[lineno] == '':  # Sometime it was already corrected
                            lines.pop(lineno)
                            changes_were_made = True

                    elif fail[2] == 'Redundant blank line at the end of a code block should be deleted.':
                        lines.pop(lineno)
                        changes_were_made = True

                    elif fail[2] == 'If an else has a brace on one side, it should have it on both' \
                            or fail[2] == 'An else should appear on the same line as the preceding }':
                        # Ignore this one
                        pass

                    elif fail[2] == '{ should almost always be at the end of the previous line':
                        regexp = regex.search("^(.*?\))[\s\t]*(const)*[\s\t]*(\/[\/\*].*)*$", lines[lineno-1])
                        if regexp is not None:
                            regexp2 = regex.search("^[\s\t]*{(.*)$", lines[lineno])
                            if regexp2 is not None:
                                lines.pop(lineno)
                                if regexp.group(2) is None:
                                    const_expr = ''
                                else:
                                    const_expr = ' ' + regexp.group(2)
                                if regexp.group(3):
                                    lines[lineno - 1] = regexp.group(1) + const_expr + ' {' + regexp.group(3) + regexp2.group(1)
                                else:
                                    lines[lineno - 1] = regexp.group(1) + const_expr + ' {' + regexp2.group(1)
                                changes_were_made = True
                            else:
                                non_corrected_lines.append(fail)
                        else:
                            non_corrected_lines.append(fail)

                    elif fail[2] == 'At least two spaces is best between code and comments':
                        regexp = regex.search("^(.*?[\s\t]*[^\"]?)(\/[\/\*][^\"]*)$", lines[lineno])
                        if regexp is not None:
                            regexp2 = regex.search("^(.*?)([\s\t]*)$", regexp.group(1))  # Remove the trailing "\s\t"
                            lines[lineno] = regexp2.group(1) + '  ' + regexp.group(2)
                            changes_were_made = True
                        else:
                            non_corrected_lines.append(fail)

                    elif fail[2] == 'Should have a space between // and comment':
                        regexp = regex.search("^(.*\/\/)([^\s].*)$", lines[lineno])
                        if regexp is not None:
                            lines[lineno] = regexp.group(1) + ' ' + regexp.group(2)
                            changes_were_made = True
                        else:
                            non_corrected_lines.append(fail)

                    elif regex.search('^(Missing spaces around )(<|<=|==|=|>=|>|!=)$', fail[2]):
                        regexp = regex.search('^(Missing spaces around )(<=|<|==|=|>=|>|!=)(.*)$', fail[2])
                        sep = regexp.group(2)
                        regexp = \
                            regex.search("^(.*[^\s\t])(" + sep + ")([^\s\t].*)$", lines[lineno])
                        if regexp is not None:
                            lines[lineno] = regexp.group(1) + ' ' + sep + ' ' + regexp.group(3)
                            changes_were_made = True
                        else:
                            non_corrected_lines.append(fail)

                    elif regex.search('^(Missing space before )({|\(|\))(.*)$', fail[2]):
                        regexp = regex.search('^(Missing space before )({|\(|\))(.*)$', fail[2])
                        sep = regexp.group(2)
                        if sep == '(':
                            regexp = regex.search("^(.*?[^\s\t])(\()(.*)$", lines[lineno])
                        elif sep == ')':
                            regexp = regex.search("^(.*?[^\s\t])(\))(.*)$", lines[lineno])
                        else:
                            regexp = regex.search("^(.*?[^\s\t])(" + sep + ")(.*)$", lines[lineno])
                        if regexp is not None:
                            # Special treatment for the regexp
                            lines[lineno] = regexp.group(1) + ' ' + regexp.group(2) + regexp.group(3)
                            changes_were_made = True
                        else:
                            non_corrected_lines.append(fail)

                    elif regex.search('^(Missing space after )(,|;|\))(.*)$', fail[2]):
                        regexp = regex.search('^(Missing space after )(,|;|\))(.*)$', fail[2])
                        sep = regexp.group(2)
                        text_regex = "^(.*?)(" + sep + ")([^\s].+)$"
                        regexp = regex.search(text_regex, lines[lineno])
                        while regexp:
                            if regexp is not None:
                                lines[lineno] = regexp.group(1) + regexp.group(2) + ' ' + regexp.group(3)
                                changes_were_made = True
                            else:
                                non_corrected_lines.append(fail)
                            regexp = regex.search(text_regex, lines[lineno])

                    elif regex.search('^(Extra space before )(\(|\)|last semicolon)(.*)$', fail[2]):
                        regexp = regex.search('^(Extra space before )(\(|\)|last semicolon)(.*)$', fail[2])
                        sep = regexp.group(2)
                        if sep == 'last semicolon':
                            sep = ';'
                        regexp = regex.search("^(.*?)([\s\t]+)(\\" + sep + ")(.*)$", lines[lineno])
                        if regexp is not None:
                            lines[lineno] = regexp.group(1) + regexp.group(3) + regexp.group(4)
                            changes_were_made = True
                        else:
                            non_corrected_lines.append(fail)

                    elif regex.search('^(Extra space after )(\(|\))(.*)$', fail[2]):
                        regexp = regex.search('^(Extra space after )(\(|\))(.*)$', fail[2])
                        sep = regexp.group(2)
                        regexp = regex.search("^(.*)(\\" + sep + ")([\s\t]+)(.*?)$", lines[lineno])
                        if regexp is not None:
                            lines[lineno] = regexp.group(1) + regexp.group(2) + regexp.group(4)
                            changes_were_made = True
                        else:
                            non_corrected_lines.append(fail)

                    elif fail[2] == 'Line ends in whitespace.  Consider deleting these extra spaces.':
                        regexp = regex.search("^(.*)([\t\s]+)$", lines[lineno])
                        if regexp is not None:
                            lines[lineno] = regexp.group(1)
                            changes_were_made = True
                        else:
                            non_corrected_lines.append(fail)

                    else:
                        non_corrected_lines.append(fail)

            # Propose some additional changes
            lines.reverse()
            for lineno, line in enumerate(lines):
                # If the = in the first section of the for loop is not surrounded
                regexp = regex.search("^([\t\s]*for[\t\s]*\(.*?)([\s\t]*)(=)([\s\t]*)(.*;.*;.*)$", line)
                if regexp is not None:
                    if regexp.group(2) == '' or regexp.group(4) == '':
                        lines[lineno] = regexp.group(1) + ' ' + regexp.group(3) + ' ' + regexp.group(5)
                        changes_were_made = True

                # There is no opening "{" with if- or for-statement on the same line
                regexp = regex.search("^([\s\t]*)((else if|if|for)[\s\t]*(\(.*\)))[\s\t]*((\/[\/\*]).*|[^{])*$", line)
                if regexp is not None:
                    # Check if parentheses are balenced
                    regexp2 = regex.search("\(([^()]|(?R))*\)", line)
                    if regexp2 and regexp2.group() == regexp.group(4):
                        # If the next line is not a comment or another loop, change it automatically,
                        # otherwise, it is probably to risky to do it automatically
                        regexp2 = regex.search("(^[\s\t]*(\/[\/\*]|for|if|while))|^[^;]*[\s\t]*$", lines[lineno-1])
                        if regexp2 is None:
                            lines[lineno] = regexp.group(1) + regexp.group(2) + ' {'
                            if regexp.group(5):
                                lines[lineno] += '  ' + regexp.group(5)
                            lines.insert(lineno-1, regexp.group(1) + '}')
                            changes_were_made = True
                        else:
                            non_corrected_lines.append(f"('{filename}', {len(lines) - lineno}, "
                                                   f"'{regexp.group(3)}-statement should have brackets on the "
                                                   f"same line', 'statement/brackets', 2)")
                regexp = regex.search("^([\s\t]*)else[\s\t]*(\/[\/\*].*|[^{i)])*$", line)
                if regexp is not None:
                    # If the next line is not a comment or another loop, change it automatically,
                    # otherwise, it is probably to risky to do it automatically
                    regexp2 = regex.search("(^[\s\t]*(\/[\/\*]|for|if|while))|^[^;]*[\s\t]*$", lines[lineno - 1])
                    if regexp2 is None:
                        lines[lineno] = regexp.group(1) + 'else {'
                        if regexp.group(2):
                            lines[lineno] += '  ' + regexp.group(2)
                        lines.insert(lineno - 1, regexp.group(1) + '}')
                        changes_were_made = True
                    else:
                        non_corrected_lines.append(f"('{filename}', {len(lines) - lineno + 1}, "
                                                   f"'else should have brackets on the same line', "
                                                   f"'statement/brackets', 2)")

                # If else is on the same line as }
                regexp = regex.search("^([\s\t]*)}[\s\t]*(else.*)$", line)
                if regexp is not None:
                    lines[lineno] = regexp.group(1) + '}'
                    lines.insert(lineno, regexp.group(1) + regexp.group(2))
                    changes_were_made = True

            lines.reverse()

            # Write the file
            if changes_were_made:
                with open(filename, 'w+') as f:
                    for lineno, line in enumerate(lines):
                        if not lineno == len(lines) - 1:
                            f.write(line + '\n')
                        else:
                            f.write(line)

        if len(non_corrected_lines) > 0:
            print("The following lines must be manually corrected")
            non_corrected_lines.reverse()
            for line in non_corrected_lines:
                print(line)
        total_non_corrected_lines += len(non_corrected_lines)

        n_files += 1
        if n_files == 30:
            exit(total_non_corrected_lines)


