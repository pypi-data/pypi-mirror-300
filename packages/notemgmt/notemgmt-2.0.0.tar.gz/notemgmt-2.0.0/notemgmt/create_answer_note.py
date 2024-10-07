import os
import argparse
import shutil

def main():
    home_dir = os.path.expanduser('~')
    vim_templates_path = os.path.join(home_dir,".vim/templates")
    skeleton_path = os.path.join(vim_templates_path, 'answer_skeleton.tex')
    parser = argparse.ArgumentParser(description="create answer note")
    parser.add_argument("--filename", type=str, required=False, default="answer")
    args = parser.parse_args()
    filename = args.filename
    ans_fn = os.path.join(os.getcwd(), f"{filename}.tex")

    if not(os.path.exists(ans_fn)):
        if not(os.path.exists(skeleton_path)):
            raise SystemExit('Answer skeleton file does not exist! Please check vim templates directory.')
        shutil.copy(skeleton_path, ans_fn)
        print('Answer file created! You may start writing your answers, Enjoy! :-D')
    else:
        raise SystemExit('Answer skeleton file already exists!')

