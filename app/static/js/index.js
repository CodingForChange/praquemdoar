$(document).ready(function(){
	
	$(document).foundation();
	
	$("li.menu-login a").click(function(event){
		event.preventDefault();
		$( ".login" ).slideToggle( "slow", function() {
			// Animation complete.
		});
	});
	
});// JavaScript Document