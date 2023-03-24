// deadline timer function
// obj refer to the direct element in html language
// endtime refer to the deadline date of the assessment
function time(obj, endTime){
    var now_time = new Date().getTime(); // get recent time
    var ddl_time =  new Date(endTime).getTime(); // get deadline time
    var msec = ddl_time - now_time; // calculate the difference in microseconds
    var time = (msec / 1000); // turn to seconds
    var day = parseInt(time / 86400); // get the days
    var hour = parseInt(time / 3600) - 24 * day; // get the hours
    var minute = parseInt(time % 3600 / 60); // get the minutes
    var second = parseInt(time % 60); // get the seconds
    // return the result to html page
    if (msec > 0) {
        obj.innerHTML="<br>Remaining：<br>"+day+" days "+hour+" hours "+minute+" minutes "+second+" seconds "+
            "<br><span>Work Hard!!!</span>"
    } else {
        obj.innerHTML="<br>The deadline has already pass.<br><span>Have you done this work?</span>"
    }
}
