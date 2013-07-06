function image_hash_ban(id) {
    var reason = prompt("WHY?", "DNP");
    if(reason) {
        $.post(
            "/postban",
            {
                "image_id": id,
                "reason": reason,
            },
            function() {
                window.location.reload();
            }
        );
    }
}

