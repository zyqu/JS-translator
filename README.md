# JS-translator
Translate API wrapped with CasperJS. Not blocked! Speed is OK.


Usage example: 
>> casperjs --ignore-ssl-errors=yes translate.js  --text="我孙子从美国回来了" --source="zh" --target="en"
>> My grandson came back from the United States

The language codes are consistent with Google Translate.

Application:
Translate the subtitle in SSA format:

python subtitle_traslate.py ssa example.ssa ar en

Dependency:
CasperJS: http://docs.casperjs.org/en/latest/installation.html

