//move .sidefig elements to the sidebar, keeping them near their original location
var moveSide = function(){
	$(".sidefig").each(function(i){
		var oldp = $(this).parent();
		$(this).removeClass("sidefig").appendTo("#sidebar").wrap('<div class="sideblock" />');
		var block = $(this).parent();
		$(this).load(function(){
			block.offset({top: oldp.offset().top - block.outerHeight() / 2, left: block.offset().left});
			});
		});
};

$(function(){
	moveSide();
});
