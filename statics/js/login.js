var phone,
	imgVerifyCode ,
	phoneVerifyCode,
	verifySuccessFlg = {
		"prompt-phone": false,
		"prompt-img": false,
		"prompt-yzm": false
	},
	phonereg = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/;
//手机号码验证
$("#phone").blur(function() {
	phone = $('#phone').val();
	if(phone === '' || null) {
		$('.prompt-phone').show().text('手机号不能为空');
		return false;
	}
	if(!phonereg.test(phone)) {
		$('.prompt-phone').show().text('手机号格式不正确');
		return false;
	}
	else if (phonereg.test(phone)) {
		$('.prompt-phone').hide();
		verifySuccessFlg["prompt-phone"] = true;
	}
});
//图形验证码验证
$("#imgVerifyCode").blur(function(){
	imgVerifyCode = $('#imgVerifyCode').val();
	if (!imgVerifyCode) {
		$('.prompt-img').show().text('图形验证码不能为空');
		return false;
	}else {
		$('.prompt-img').hide();
		verifySuccessFlg["prompt-img"] = true;
	}
});
//手机验证码验证
$("#phoneVerifyCode").blur(function(){
	phoneVerifyCode = $('#phoneVerifyCode').val();
	console.log(phoneVerifyCode)
	if(!phoneVerifyCode) {
		$('.prompt-yzm').show().text('手机验证码不能为空');
		return false;
	}else {
		$('.prompt-yzm').hide();
		verifySuccessFlg["prompt-yzm"] = true;
	}
});
//点击验证码刷新



//获取手机验证码
$("#captcha-btn").on('click',function(){
    $.post('/confirm',{capthca: phoneVerifyCode},function (data){
            if(data.code == 200){
            	
            }
            if(data.code == 201){
            	$('.prompt-yzm').text('手机验证码错误');
            }
      });
    
});

//提交
$('.login-button').on('click',function (){
	var isSuccessFlg = true;
	for (key in verifySuccessFlg) {
		if (!verifySuccessFlg[key]) {
			$('.' + key).show();
			isSuccessFlg = false;
		}
	}
	
	if (!isSuccessFlg) {
		return;
	}
	
	//do login
});
