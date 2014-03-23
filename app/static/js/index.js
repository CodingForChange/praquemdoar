$(document).ready(function(){
	

	$(document).foundation();		

	setTimeout( formataTwitter,2000 );

	
	$("li.menu-login a").on("click" , function(event){
		event.preventDefault();
		$( ".login" ).slideToggle( "slow", function() {
			// Animation complete.
		});
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
