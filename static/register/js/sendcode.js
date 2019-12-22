var but=document.getElementById('but_ver_email');
var email=document.getElementById('form-email');

but.onclick=()=>{
    but.disabled=true;
    $.ajax({
        url:'/register/sendmail',
        type:'POST',
        data:{'email':email.value},
    });
};