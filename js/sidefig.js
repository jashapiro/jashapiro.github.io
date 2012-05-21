//move .sidefig elements to the sidebar, keeping them near their original location
var moveSide = function(){
	var min_offset = 0;
	$(".align-sidebar img").each(function(i){
		var oldp = $(this).parent();
		$(this).appendTo("#sidebar").wrap('<div class="sideblock" />');
		var block = $(this).parent();
		$(this).load(function(){
			offset =  Math.max(min_offset, 
							   oldp.offset().top - block.outerHeight() / 2);
			block.offset({top: offset, left: block.offset().left});
			min_offset = offset + block.outerHeight();
			});
		});
};

$(function(){
	moveSide();
});
