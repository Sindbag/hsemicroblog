$('#create-post-btn').on('click', function(event){
    event.preventDefault();
    console.log("post is sent!!")  // sanity check
    create_post();
});

$('.liker').on('click', function() {
    if ($(this).hasClass('like_button')) {
        method = 'like'
    } else {
        method = 'dislike'
    }
    like_post($(this), $(this).parent().data('id'), method);
});

$('.answer-button').on('click', function(){
    $(this).disable;
    post_id = $(this).parent().parent().siblings('div.likepoint').data('id');
    $.ajax({
        url : '/create_answer/',
        method : 'GET',
        data : { 'post_id' : post_id },

        success : function(text) {
            $('div.overlay').append(text).toggle();
            $(this).enable;
        },

        error : function(xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});

function SetEventListenerFollow() {
    $('.followman').on('click', function() {
        user_id = $(this).data('id');
        follow(user_id, 'follow', $(this));
        SetEventListenerUnFollow();
    });
}

function SetEventListenerUnFollow() {
    $('.unfollowman').on('click', function() {
        user_id = $(this).data('id');
        follow(user_id, 'unfollow', $(this));
        SetEventListenerFollow();
    });
}

SetEventListenerFollow();
SetEventListenerUnFollow();

$('a.unfollowbig').on('click', function() {
    user_id = $(this).data('id');
    follow(user_id, 'unfollow', $(this));
    $(this).parents('div.bigfollower').remove();
});

function follow(user_id, method, obj) {
    if (method == 'follow') {
        old = 'followman', newer = 'unfollowman', old_icon = 'glyphicon-check', newer_icon = 'glyphicon-remove', url='/follow/';
    } else {
        old = 'unfollowman', newer = 'followman', old_icon = 'glyphicon-remove', newer_icon = 'glyphicon-check', url='/unfollow/';
    }
    $.ajax({
        url : url,
        method : 'POST',
        data : { 'user_id' : user_id, 'method' : method },

        success : function(text) {
            obj.removeClass(old).addClass(newer).children('span').removeClass(old_icon).addClass(newer_icon);
        },

        error : function(xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$('div.overlayoff').on('click', function() {
    $(this).siblings('#answer-wrapper').remove();
    $(this).parent().hide();
});


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function create_post() {
    $.ajax({
        url : "/create_post/", // the endpoint
        type : "POST", // http method
        data : { text : $('#create_post_text').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#create_post_text').val(''); // remove the value from the input
            console.log("success"); // another sanity check
            // $('#flow').prepend("<h4><a href='" + json.author_link + "'>" + json.author + "</a> on " + json.created + "</h4>" +
            // "<a href=\"" + json.post_link + "\"><span class=\"glyphicon glyphicon-resize-full\" aria-hidden=\"true\"></span></a>" +
            // "<pre>" + json.text + "</pre>");
            window.location = json.post_link;
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function create_answer() {
    $.ajax({
        url : "/create_post/", // the endpoint
        type : "POST", // http method
        data : { text : $('#create_answer_text').val(), ansfor : $('#ansfor').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#create_post_text').val(''); // remove the value from the input
            console.log("success"); // another sanity check
            // $('#flow').prepend("<h4><a href='" + json.author_link + "'>" + json.author + "</a> on " + json.created + "</h4>" +
            // "<a href=\"" + json.post_link + "\"><span class=\"glyphicon glyphicon-resize-full\" aria-hidden=\"true\"></span></a>" +
            // "<pre>" + json.text + "</pre>");
            window.location = json.post_link;
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function like_post(object, id, method) {
    if (object.hasClass('like_button')) {
        object.removeClass('like_button').addClass('dislike_button').children('span.likepic').removeClass('disliked').addClass('liked');
    } else {
        object.removeClass('dislike_button').addClass('like_button').children('span.likepic').removeClass('liked').addClass('disliked');
    }
    $.ajax({
        url : "/like_post/" + id + '/',
        type : "POST",
        data : { method : method, post_id : id},

        success : function(json) {
            object.siblings('span.post_likes').text(json.likes + ' ');
        },

        error : function(xhr, errmsg, err) {
            if (object.hasClass('like_button')) {
                object.removeClass('like_button').addClass('dislike_button').children('span.likepic').addClass('liked');
            } else {
                object.removeClass('dislike_button').addClass('like_button').children('span.likepic').removeClass('liked');
            }
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};