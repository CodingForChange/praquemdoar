$(document).ready(function(){
	

	$(document).foundation();		

	setTimeout( formataTwitter,2000 );

	
	$("li.menu-login a").click(function(event){
		event.preventDefault();
		$( ".login" ).slideToggle( "slow", function() {
			// Animation complete.
		});
	});
	
});// JavaScript Document

formataTwitter = function()
{
	// $("iframe").contents().find(".timeline-header").hide();
	conteudo = '<span style="font-size: 14px;"><i class="fa fa-twitter"></i> '+
	'Acompanhe pelo Twitter as últimas solicitações </span><br />'+
	'<div style="font-size: 26px;font-weight: normal;padding-top: 5px;">@praquemdoar</div>';

	$("iframe").contents().find(".timeline-header").html(conteudo);
};
