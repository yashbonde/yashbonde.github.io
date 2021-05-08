#!/usr/bin/python3

import os
import re
import sys
from copy import deepcopy
from argparse import ArgumentParser

# ========== MARKDOWN FUNCTIONS ========== #

def generic_parse_string(string):
  # generic parser for header string and para strings
  # returns {
  #   "text": <clean text>,
  #   "spans": [{
  #     "start": <int>,
  #     "end": <int>,
  #     "type": <code/link>,
  #     "link": <link/None>
  #   }]
  # }
  string = re.sub('\s+', " ", string.strip())
  target_string = deepcopy(string)

  # first extract bold
  for x in re.findall(r"\*{2}((<|>|\'|\"|\w|\s)*)\*{2}", string):
    seq = x[0].strip()
    repl = f"<b>{seq}</b>"
    target_string = target_string.replace(f"**{seq}**", repl)

  # then extract italics
  for x in re.findall(r"\*((<|>|\'|\"|\w|\s)*)\*", string):
    seq = x[0].strip()
    repl = f"<i>{seq}</i>"
    target_string = target_string.replace(f"*{seq}*", repl)

  # then extract strikethroughs
  for x in re.findall(r"~+((<|>|\'|\"|\w|\s)*)~+", string):
    seq = x[0].strip()
    repl = f"<strike>{seq}</strike>"
    target_string = target_string.replace(f"~~{seq}~~", repl)

  # then replace Links
  for x in re.findall(r"\[(.*)\]\((.*)\)", string):
    cap = x[0].strip()
    url = x[1].strip()
    repl = f'<a href="{url}" class="article-a">{cap}</a>'
    seq = f"[{cap}]({url})"
    target_string = target_string.replace(seq, repl)

  # inline code
  for x in re.findall(r"\`([^\`].*?)\`", string):
    repl = f'<code>{x.strip()}</code>'
    target_string = target_string.replace(f"`{x}`", repl)

  return {"text": target_string}

def parse_lines(text):
  # this function takes in the raw file string and returns the sections
  # in form of a list. Each object in the list has the following format:
  # {
  #   "type": "p",
  #   "content": "Well this is some BS paragraph about how India is poor",
  #   "links": [{"start": 4, "end": 5, "link": "some/nice/link.html"}]
  # }
  #
  # the way to go about it is as follows:
  # - get the code that is present in ```...``` (codeblock order below)
  #   and remove that from the string because it can cause problems later
  # - split the text into sections by "\n\n"
  # - parse this text and determine the types
  sections = []
  
  codeblocks = re.split("```", text)
  if len(codeblocks) > 1:
    # ``` has some problem in regex, so manually built this
    assert (len(codeblocks)-1) % 2 == 0, "codeblocks not correct, missed ```?"
    codeblocks = [f"```{codeblocks[i]}```" for i in range(1, len(codeblocks), 2)]
    for c in codeblocks:
      text = text.replace(c, "<|codeblock|>")

  # splitting by \n\n+ also remove accidental multiple newlines
  simple_splits = re.split("\n\n+", text)
  code_cntr = 0
  for x in simple_splits:
    x = x.strip()
    # clause for code that has been removed above
    if x == "<|codeblock|>":
      text = codeblocks[code_cntr].replace("`", "").strip()
      sections.append({"type": "codeblock", "text": text})
      code_cntr += 1
      continue
    
    # is this a header?
    header = re.match(r"^#+\s(.*)$", x)
    if header is not None:
      parsed_string = generic_parse_string(header.group(1))
      header_level = len(re.findall(r"#", x))
      sections.append({"type":f"h{header_level}", **parsed_string})
      continue

    # is this a list?
    list_items = re.findall(r"\n(-|\*)", x)
    if list_items:
      list_items = re.split(r"\n(-|\*)", x)
      if list_items[0][0] not in ['-', '*']:
        parsed_string = generic_parse_string(list_items[0])
        sections.append({"type":"p", **parsed_string})
        list_items = list_items[1:]
      for i, item in enumerate(list_items):
        if i % 2 == 0:
          continue
        parsed_string = generic_parse_string(item)
        sections.append({"type":"li", **parsed_string})
      continue

    # is this an image or some link?
    image_link = re.match(r"!\[((.|\n)*)\]\((.*)\)", x)
    if image_link is not None:
      parsed_string = generic_parse_string(image_link.groups()[0])
      _weblink = image_link.groups()[-1]
      sections.append({"type": "figure", "src": _weblink})
      # sections.append({"type": "figcaption", "text": get_figcaption(parsed_string, _weblink)})
      sections.append({"type":"figcaption", **parsed_string, "url": _weblink})
      continue

    # is this a quote?
    if x[:2] == "> ":
      x = re.sub("\n?>+", "\n", x)
      x = generic_parse_string(x)
      sections.append({"type":"blockquote", **x})
      continue
    
    # if it is not a codeblock/quote/list/link/header then it's a para
    x = generic_parse_string(x)
    sections.append({"type": "p", **x})
  
  return sections


# ============ HTML FUNCTIONS ============ #

def get_header(title):
  return f"""
  <meta charset="utf-8">

  <title>{title}</title>

  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Poppins:100,400,700" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Serif:300,400,400i,600,600i,700,700i,800" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Ubuntu+Mono:400,400i,700,700i" rel="stylesheet">
  

  <!-- Link the main.css stylesheet -->
  <link href="styles/reset.css" rel="stylesheet">
  <link href="styles/-debug.css" rel="stylesheet">
  <link href="styles/article.css" rel="stylesheet">
  <link href="styles/article-text.css" rel="stylesheet">
  <link href="styles/article-figure.css" rel="stylesheet">
  <link href="styles/nav.css" rel="stylesheet">
  <link href="styles/code-block.css" rel="stylesheet">
  <link href="styles/footer-blog.css" rel="stylesheet">
"""

def get_time_string():
  from datetime import datetime
  d = datetime.now()
  _d = d.strftime("%d-%m-%Y")
  _m = {
    "01": "JAN.",
    "02": "FEB",
    "03": "MAR",
    "04": "APR",
    "05": "MAY",
    "06": "JUNE",
    "07": "JULY",
    "08": "AUG",
    "09": "SEP",
    "10": "OCT",
    "11": "NOV",
    "12": "DEC"
  }[d.strftime("%m")]
  _d_str = f"{_m} {d.strftime('%d')} {d.strftime('%Y')}"
  return f'<time datetime="{_d}">{_d_str}</time>'

def get_footer():
  return """<p class="footer-p">
        CONNECT WITH ME
    </p>
    <div class = "share">
        <a href="https://www.linkedin.com/in/yash-bonde/"><img src="images/linkedin.svg"></a>
        <a href="https://www.instagram.com/yassh.bonde/"><img src="images/instagram.svg"></a>
    </div>"""


def get_body(sections):
  # first get the correct section codes
  section_codes = []
  for x in sections:
    if x["type"] not in ["codeblock", "figcaption", "figure"]:
      code = f"""<{x["type"]}>
  {x["text"]}
</{x["type"]}>"""

    elif x["type"] == "codeblock":
      code = f"""<pre><code>
  {x["text"]}
</code></pre>"""

    elif x["type"] == "figcaption":
      text = x["text"]
      if "https" in x["url"]:
        to_add = ""
        if text[-1] != ".":
          to_add += "."
        text += f'{to_add} From <a href={x["url"]} class="article-a">here</a>'
      figcaption = f"""<figcaption>
  <p>
    {text}
  </p>
</figcaption>"""
      code = figcaption

    elif x["type"] == "figure":
      code = f"""<figure class="size-2">
  <img src="{x["src"]}">
</figure>"""

    section_codes.append(code)
  
  # combine get body
  start_header = "\n".join(section_codes[:2])
  time_string = get_time_string()
  start_header += f"\n{time_string}"

  body = "\n\n".join(section_codes[2:])
  body = f"""<nav>
      <a class = "nav-home" href="../index.html">HOME</a>
      <a class = "nav-project" href="../projects.html">PROJECTS</a>
      <a class = "nav-blog" href="../musings.html">BLOG</a>
      <a class = "nav-resume" href="../files/yashbonde_resume.pdf">RESUME</a>
  </nav>

  <article id = "blog-0">

    {start_header}

    {body}
  
  </article>
"""
  return body


def convert_to_html(sections):
  # this function takes in the parsed sections from parse_lines(...) func
  # and stitches together a webpage as a single string.
  title = list(filter(lambda x: "h" in x["type"], sections))[0]
  header = get_header(title["text"])
  body = get_body(sections)
  footer = get_footer()
  
  return f"""<!DOCTYPE html>
<!-- This is an autogenerated file from @yashbonde/md2html -->
<!-- find it cool, check it out on Github -->

<html>
  <head>
    {header}
  </head>

  <body>
    {body}
  </body>

  <footer>
    {footer}
  </footer>
</html>
"""

if __name__ == "__main__":
  args = ArgumentParser(description="Converts markdown to my HTML code")
  args.add_argument("input", type = str, help = "markdown file path")
  args.add_argument("output", type = str, help = "Output filename")
  args = args.parse_args()

  inpath_full = os.path.abspath(args.input)
  here = os.path.dirname(os.path.abspath(__file__))
  blogs_folder = os.path.join(here, "blogs")
  output_file = os.path.join(blogs_folder, args.output)
  if not output_file.endswith(".html"):
    output_file += ".html"

  print("Reading file:", inpath_full)
  print("Output file:", output_file)

  # open the markdown file -> parse -> stitch -> save
  with open(inpath_full, "r") as f:
    lines = f.read()
  parsed_data = parse_lines(lines)
  html_str = convert_to_html(parsed_data)
  with open(output_file, "w") as f:
    f.write(html_str)
