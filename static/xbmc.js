function GetNowPlaying() {
	$.ajax({
		url: "/json/viewcommand",
		type: "POST",
		data: {
			deviceid: deviceID,
			command: "nowplaying"
		}
	})
	.done(function(data) {
		$("#nptitle").text(data.item.title);
		$("#nptype").text(data.item.type);
	})
	.fail(function() {
		alert("Failed to get data. Please try again.");
	});
}