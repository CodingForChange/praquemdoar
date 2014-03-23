$(document).ready(function(){
	

	$(document).foundation();		

	setTimeout( formataTwitter,2000 );

	
	$("li.menu-login a").on("click" , function(event){
		event.preventDefault();
		$( ".login" ).slideToggle( "slow", function() {
			// Animation complete.
		});
	});

	$("#contato-inst").on("click", function () {
		$("#bl-contato").slideToggle( "slow", function() {
			// Animation complete.
		});
	});
	
	jQuery.validator.addMethod("cnpj", function(cnpj, element) {
		cnpj = jQuery.trim(cnpj);// retira espaços em branco
		// DEIXA APENAS OS NÚMEROS
		cnpj = cnpj.replace('/','');
		cnpj = cnpj.replace('.','');
		cnpj = cnpj.replace('.','');
		cnpj = cnpj.replace('-','');
	      console.log(cnpj);
		var numeros, digitos, soma, i, resultado, pos, tamanho, digitos_iguais;
		digitos_iguais = 1;
	      
		if (cnpj.length < 14 && cnpj.length < 15){
		   return false;
		}
		for (i = 0; i < cnpj.length - 1; i++){
		   if (cnpj.charAt(i) != cnpj.charAt(i + 1)){
		      digitos_iguais = 0;
		      break;
		   }
		}
	      
		if (!digitos_iguais){
		   tamanho = cnpj.length - 2
		   numeros = cnpj.substring(0,tamanho);
		   digitos = cnpj.substring(tamanho);
		   soma = 0;
		   pos = tamanho - 7;
	      
		   for (i = tamanho; i >= 1; i--){
		      soma += numeros.charAt(tamanho - i) * pos--;
		      if (pos < 2){
			 pos = 9;
		      }
		   }
		   resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
		   if (resultado != digitos.charAt(0)){
		      return false;
		   }
		   tamanho = tamanho + 1;
		   numeros = cnpj.substring(0,tamanho);
		   soma = 0;
		   pos = tamanho - 7;
		   for (i = tamanho; i >= 1; i--){
		      soma += numeros.charAt(tamanho - i) * pos--;
		      if (pos < 2){
			 pos = 9;
		      }
		   }
		   resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
		   if (resultado != digitos.charAt(1)){
		      return false;
		   }
		   return true;
		}else{
		   return false;
		}
	}, "Informe um CNPJ válido."); // Mensagem padrão
	$("#cnpj").mask("999.999.999/9999-99");
	$("#form_login").validate({
		rules: {
		   cnpj: {required: true, cnpj: true},
		   senha: "required",
                    confirmacao: {
                      equalTo: "#senha"
                    }
		},
		messages: {		   
		   cnpj: { cnpj: 'CNPJ inválido'}
		}
		,submitHandler:function(form) {
		   //$("#form-login").submit();
		}
	});
	
	$("#upload-file-container").on("click",function(event){
		event.stopPropagation();
		$("#logo").trigger('click');
		$("#logo").change(function(){
			$("#logo_hidden").val($(this).val());
		});
		return false;
	});
	
	
});// JavaScript Document

formataTwitter = function()
{
	// $("iframe").contents().find(".timeline-header").hide();
	conteudo = '<div style="float: left; margin: 5px;margin-right: 10px;"><img src="static/img/twitter.png"></div><span style="font-size: 14px;"> '+
	'Acompanhe pelo Twitter as últimas solicitações </span><br />'+
	'<div style="font-size: 26px;font-weight: normal;padding-top: 5px;">@praquemdoar</div>';

	conteudo_footer = '<div style="text-align: right;">Seguir <a style="color: #C27CA5" href="http://twitter.com/praquemdoar">@praquemdoar</a></div>';

	$("iframe").contents().find(".timeline-header").html(conteudo);

	$("iframe").contents().find(".timeline-footer").html(conteudo_footer);

	$("iframe").contents().find(".load-more").hide();

};
