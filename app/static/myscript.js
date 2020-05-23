//search dropdown button
dropdown_options = {
    hover: true,
    alignment: 'right',
    constrainWidth: false
};

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, dropdown_options);
});

carousel_options = {
    numVisible: 3,
    fullWidth: true,
    indicators: true,
    noWrap: true,
    dist: 0
};

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.carousel');
    var instances = M.Carousel.init(elems, carousel_options);
});

//sidenav
document.addEventListener('DOMContentLoaded', function()
{
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {});
});

$(document).ready(function(e){

    // Search Box
    $('.search_row .dropdown-content').find('a').click(function(e) {
        e.preventDefault();
        var category = $(this).children()[1].innerHTML;
        $('#search_box').val("");
        $("#search_box").attr('disabled', false);
        $("#search_box").attr('placeholder', "Search " + category);
        $("#hidden_category").val(category);
    });

    $('.modal').modal();
});

function checkfollowing(id) {
    var btn = document.getElementById(id);
    btn.value = 'Followed';
    btn.innerHTML = 'Followed';
}

function check_like(id) {
    var btn = document.getElementById(id);
    btn.value = 'Liked';
    btn.innerHTML = 'Liked';
}


function checkfollowing_prof_stud(id) {
    var btn = document.getElementById(id);
    btn.value = 'Followed';
    btn.innerHTML = 'Followed';
}
function checkfollowing_stud_stud(id) {
    var btn = document.getElementById(id);
    btn.value = 'Followed';
    btn.innerHTML = 'Followed';
}

function checkfollowing_prof_prof(id) {
    var btn = document.getElementById(id);
    btn.value = 'Followed';
    btn.innerHTML = 'Followed';
}
function checkfollowing_stud_prof(id) {
    var btn = document.getElementById(id);
    btn.value = 'Followed';
    btn.innerHTML = 'Followed';
}

function set_following(id,num) {
    // alert(id,num);
    var temp = 'followers_'+id;
    console.log(temp,num);
    document.getElementById(temp).innerHTML = num + ' Followers';
}

function set_following_profs(id,num) {
    // alert(id,num);
    var temp = 'prof_follow_'+id;
    document.getElementById(temp).innerHTML = '<b>Followers:</b> '+num;
}
function set_following_studs(id,num) {
    // alert(id,num);
    var temp = 'stud_follow_'+id;
    document.getElementById(temp).innerHTML = '<b>Followers:</b> '+num;
}

function set_following_mystuds(id,num) {
    // alert(id,num);
    var temp = 'mystud_follow_'+id;
    document.getElementById(temp).innerHTML = '<b>Followers:</b> '+num;
}

function set_following_myprofs(id,num) {
    // alert(id,num);
    var temp = 'myprof_follow_'+id;
    document.getElementById(temp).innerHTML = '<b>Followers:</b> '+num;
}

function set_following_labs(id,num) {
    // alert(id,num);
    var temp = 'lab_follow_'+id;
    document.getElementById(temp).innerHTML = '<b>Followers:</b> '+num;
}

function set_search_following_studs(id,num) {
    // alert(id,num);
    var temp = 'search_stud_follow_'+id;
    document.getElementById(temp).innerHTML = num + '<b> Followers</b> ';
}

function set_search_following_profs(id,num) {
    // alert(id,num);
    var temp = 'search_prof_follow_'+id;
    document.getElementById(temp).innerHTML = num + '<b> Followers</b> ';
}

function set_search_following_labs(id,num) {
    // alert(id,num);
    var temp = 'search_lab_follow_'+id;
    document.getElementById(temp).innerHTML = num + '<b> Followers</b> ';
}

function follow_lab(id) {
    var btn = document.getElementById(id);
    if (btn.value == "Follow") {
        $.ajax({
            url: '/follow_lab/' + id,
            success: function (resp) {
                var temp = "followers_" + id;
                document.getElementById(temp).innerHTML = resp + ' Followers';
            }
        });
        btn.value = 'Followed';
        btn.innerHTML = 'Followed';
    }
    else {
        $.ajax({
            url: '/unfollow_lab/' + id,
            success: function (resp) {
                var temp = "followers_" + id;
                document.getElementById(temp).innerHTML = resp + ' Followers';
            }
        });

        btn.value = 'Follow';
        btn.innerHTML = 'Follow';

    }
}

function search_follow_lab(id) {
    var btn = document.getElementById(id);
    if (btn.value == "Follow") {
        $.ajax({
            url: '/follow_lab/' + id,
            success: function (resp) {
                var temp = "search_lab_follow_"+id;
                document.getElementById(temp).innerHTML = resp + ' Followers';
            }
        });
        btn.value = 'Followed';
        btn.innerHTML = 'Followed';
    }
    else {
        $.ajax({
            url: '/unfollow_lab/' + id,
            success: function (resp) {
                var temp = 'search_lab_follow_'+id;
                document.getElementById(temp).innerHTML = resp + ' Followers';
            }
        });

        btn.value = 'Follow';
        btn.innerHTML = 'Follow';
    }
}



function follow_student(id) {
    var btn = document.getElementById(id);
    if (btn.value == "Follow") {
        $.ajax({ url: '/follow_student/' + id,
        success: function (resp) {
            var temp = "search_stud_follow_" + id;
            console.log(temp)
            document.getElementById(temp).innerHTML = resp + ' Followers';
        }
        });
        btn.value = 'Followed';
        btn.innerHTML = 'Followed';
    }
    else {
        $.ajax({ url: '/unfollow_student/' + id,
        success: function (resp) {
            var temp = "search_stud_follow_" + id;
            document.getElementById(temp).innerHTML = resp + ' Followers';
        }
        });
        btn.value = 'Follow';
        btn.innerHTML = 'Follow';

    }
}


function follow_professor(id) {
    var btn = document.getElementById(id);
    if (btn.value == "Follow") {
        $.ajax({ url: '/follow_professor/' + id ,
        success: function (resp) {
            var temp = "search_prof_follow_" + id;
            console.log(resp)
            document.getElementById(temp).innerHTML = resp + ' Followers';
        }
        });
        btn.value = 'Followed';
        btn.innerHTML = 'Followed';
    }
    else {
        $.ajax({ url: '/unfollow_professor/' + id ,
        success: function (resp) {
            var temp = "search_prof_follow_" + id;
            console.log(resp)
            document.getElementById(temp).innerHTML = resp + ' Followers';
        }
        });
        btn.value = 'Follow';
        btn.innerHTML = 'Follow';

    }
}

function like_pub(id) {
    var btn = document.getElementById(id);
    if (btn.value == "Like") {
        $.ajax({
            url: '/like_pub/' + id,
            success: function (resp) {
                var temp = "likes_" + id;
                document.getElementById(temp).innerHTML = resp + ' Likes';
            }
        });
        btn.value = 'Liked';
        btn.innerHTML = 'Liked';
    }
    else {
        $.ajax({
            url: '/unlike_pub/' + id,
            success: function (resp) {
                var temp = "likes_" + id;
                document.getElementById(temp).innerHTML = resp + ' Likes';
            }
        });

        btn.value = 'Like';
        btn.innerHTML = 'Like';

    }
}

function add_student(id) {
    var tempid = id.substring(5);
    var btn = document.getElementById(id);
    if (btn.value == 'Add To "My Students"') {
        $.ajax({
            url: '/add_student/' + tempid });
        btn.value = 'Added To "My Students"';
        btn.innerHTML = 'Added To "My Students"';
    }
    else {
        $.ajax({
            url: '/remove_student/' + tempid });

        btn.value = 'Add To "My Students"';
        btn.innerHTML = 'Add To "My Students"';

    }
}

function add_professor(id) {
    var tempid = id.substring(5);
    var btn = document.getElementById(id);
    if (btn.value == 'Add To "My Guides"') {
        $.ajax({
            url: '/add_professor/' + tempid });
        btn.value = 'Added To "My Guides"';
        btn.innerHTML = 'Added To "My Guides"';
    }
    else {
        $.ajax({
            url: '/remove_professor/' + tempid });

        btn.value = 'Add To "My Guides"';
        btn.innerHTML = 'Add To "My Guides"';

    }
}

function add_lab(id) {
    var btn = document.getElementById(id);
    var index = id.substring(4);
    console.log(index);

    if (btn.value == "Add To My Labs") 
    {
        $.ajax({
        url: '/add_lab/' + index, 
        success: function (resp) {
        console.log(resp);
        }});
        btn.value = "Added To Your Labs";
        btn.innerHTML = 'Added To Your Labs';
    }
    else 
    {
        $.ajax({ 
        url: '/remove_lab/' + index,
        success: function (resp) {
        console.log(resp);
        }});
        btn.value = 'Add To My Labs';
        btn.innerHTML = 'Add To My Labs';
    endif;
    }
}

function check_add_lab(id) {
    var temp = "lab_"+id;
    var btn = document.getElementById(temp);
    btn.value = 'Added To Your Labs';
    btn.innerHTML = 'Added To Your Labs';
}

function check_add_stud(id) {
    var temp = "stud_"+id;
    var btn = document.getElementById(temp);
    btn.value = 'Added To "My Students"';
    btn.innerHTML = 'Added To "My Students"';
}
function check_add_prof(id) {
    var temp = "prof_"+id;
    var btn = document.getElementById(temp);
    btn.value = 'Added To "My Guides"';
    btn.innerHTML = 'Added To "My Guides"';
}