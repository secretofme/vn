// function findStr(str,n){
// 		var temp=0;
// 		for(var i=0;i<str.length;i++){
// 			if(str.charAt(i)==n){
// 				temp++;
// 			};
// 		};
// 		return temp;
// 	};
// 	window.onload=function() {
// 		var userName=document.getElementById("userName");
// 		var psd=document.getElementById("psd");
// 		var psd1=document.getElementById("psd1");
// 		var unmInfo=document.getElementsByClassName('unmInfo')[0];
// 		var count=document.getElementsByClassName('count')[0];
// 		var psdInfo=document.getElementsByClassName('psdInfo')[0];
// 		var psd1Info=document.getElementsByClassName('psd1Info')[0];
// 		var fl=document.getElementsByClassName("fl")[0];
// 		var name_length=0;
// 		var reg=/[^\w\u4e00-\u9fa5]/g;
// 		var re_n=/[^\d]/g;
// 		var re_t=/[^a-zA-Z]/g
// 		userName.onfocus=function(){
// 			unmInfo.style.display="inline-block";
// 			unmInfo.innerHTML='<i class="warn"></i> 6-16个字符，请使用字母加数字或者符号，不能单独使用字母 数字或者字符。'
// 		}
// 		userName.onkeyup=function(){
// 			count.style.visibility="visible";
// 			name_length=getLength(this.value);
// 			count.innerHTML=name_length+"个字符";
// 			if(name_length==0){
// 				count.style.visibility="hidden";
// 			}
// 		}
// 		userName.onblur=function(){
// 			if(reg.test(this.value)){
// 				unmInfo.innerHTML='<i class="cuo"></i>含有非法字符';
// 			}else if(this.value==""){
// 				unmInfo.innerHTML='<i class="cuo"></i>不能为空';
// 			}else if(name_length>25){
// 				unmInfo.innerHTML='<i class="cuo"></i>长度超过25个字符';
// 			}else if(name_length<6){
// 				unmInfo.innerHTML='<i class="cuo"></i>长度少于6个字符';
// 			}else{
// 				unmInfo.innerHTML='<i class="right"></i>OK!';
// 			}
// 		}
//
// 		psd.onfocus=function(){
// 			psdInfo.style.display="inline-block";
// 			psdInfo.innerHTML='<i class="warn"></i> 6-16个字符，请使用字母加数字或者符号，不能单独使用字母 数字或者字符。';
// 		}
// 		psd.onkeyup=function(){
// 			if(this.value.length>5){
// 				fl.className="active";
// 				psd1.removeAttribute("disabled");
// 				psd1Info.style.display="inline-block";
// 				psd1Info.innerHTML='<i class="warn"></i> 再输入一次';
// 			}else{
// 				fl.className="";
// 				psd1.setAttribute("disabled","disabled");
// 				psd1Info.style.display="none";
// 				psd1.value="";
// 			}
// 			if(this.value.length>10){
// 				fl.className="active1";
// 			}else{
// 				fl.className="";
// 				psd1.value="";
// 			}
//
// 		}
// 		psd.onblur=function(){
// 			var m=findStr(this.value,this.value[0]);
// 			if(this.value==""){
// 				psdInfo.innerHTML='<i class="cuo"></i> 不能为空';
// 			}else if(m==this.value.length){
// 				console.log(1);
// 				psdInfo.innerHTML='<i class="cuo"></i> 不能有相同字符';
// 			}else if(this.value.length<6||this.value.length>16){
// 				psdInfo.innerHTML='<i class="cuo"></i> 长度应为6-16个字符';
// 			}else if(!re_n.test(this.value)){
// 				psdInfo.innerHTML='<i class="cuo"></i> 不能全为数字';
// 			}else if(!re_t.test(this.value)){
// 				psdInfo.innerHTML='<i class="cuo"></i> 不能全为字母';
// 			}else{
// 				psdInfo.innerHTML='<i class="right"></i> OK';
// 			}
// 		}
//
// 		psd1.onblur=function(){
// 			if(this.value!=psd.value){
// 				psd1Info.innerHTML='<i class="cuo"></i> 两次输入的密码不一致';
// 			}else{
// 				psd1Info.innerHTML='<i class="right"></i> OK';
// 			}
// 		}
// 	}
// 	function getLength(str){
// 		return str.replace(/[^\x00-xff]/g,"xx").length;
// 	}

function checkpassword() {
        var password = document.getElementById("psd").value;
        var repassword = document.getElementById("psd1").value;

        if(password == repassword) {
            document.getElementById("tishi").innerHTML='<i class="right"></i> OK';
            document.getElementById("submit").disabled = false;

        }else {
            document.getElementById("tishi").innerHTML='<i class="right"></i> 输入密码不一致!';
            document.getElementById("submit").disabled = true;
        }
    }