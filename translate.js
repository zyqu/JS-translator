#!/usr/bin/env node

//Zhengyang QU, 2016-1-17
//Usage example: casperjs --ignore-ssl-errors=yes translate.js  --text="我孙子从美国回来了" --source="zh" --target="en"
//>> My grandson came back from the United States

var casper = require("casper").create()
casper.userAgent ( 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36' );

format = require("utils").format
var source = casper.cli.get("source")
var target = casper.cli.get("target")
var text = casper.cli.get("text")

var url = format("https://translate.google.com/?hl=en&eotf=1&sl=%s&tl=%s#%s/%s/%s", source, target, source, target, text)

casper.start(url,  function(response){
	this.waitForSelector("#result_box", function(){
		this.click('input[id="gt-submit"]');
		this.wait(2000, function(){
			if (this.exists('span[class="hps"]')){
				restext = this.fetchText("#result_box");
				console.log(restext);
			}else{
				console.log("ERROR");
			}
		});
	}, function(){
		console.log("ERROR");
	}, 5000);
});

casper.run();

