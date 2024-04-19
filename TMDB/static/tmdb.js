if (window.location.pathname.indexOf('/account/') === 0) {
    document.addEventListener('DOMContentLoaded', () => {
        var x_movie_genre_names = JSON.parse(document.getElementById("movie_pie_genre_names").innerHTML);
        var y_movie_genre_numbers = JSON.parse(document.getElementById("movie_pie_genre_numbers").innerHTML);
        var x_tv_genre_names = JSON.parse(document.getElementById("tv_pie_genre_names").innerHTML);
        var y_tv_genre_numbers = JSON.parse(document.getElementById("tv_pie_genre_numbers").innerHTML);
        var barColors = [
        "#b91d47",
        "#00aba9",
        "#2b5797",
        "#e8c3b9",
        "#1e7145"
        ];
        new Chart("movie_chart", {
        type: "pie",
        data: {
            labels: x_movie_genre_names,
            datasets: [{
            backgroundColor: barColors,
            data: y_movie_genre_numbers
            }]
        },
        options: {
            title: {
            display: true,
            text: "Top 5 genres in your movie list"
            }
        }
        });
        new Chart("tv_chart", {
            type: "pie",
            data: {
                labels: x_tv_genre_names,
                datasets: [{
                backgroundColor: barColors,
                data: y_tv_genre_numbers
                }]
            },
            options: {
                title: {
                display: true,
                text: "Top 5 genres in your TV show list"
                }
            }
            });
    });
}

function editWatchStatus(relative_url, media_type, media_id) {
    const watch_status_message = document.getElementById("watch_status_p");
    fetch(`/${relative_url}/${media_type}/${media_id}/`)
    .then (response => response.json())
    .then (response => {
        console.log(response.message);
        watch_status_message.innerHTML = response.watch_status;
    })
}

function addList(media_type, media_id){
    watchlist_option = document.getElementById("select_watchlist").value;
    if (watchlist_option === "watching") {
        editWatchStatus("add_watching", media_type, media_id);
    } else if (watchlist_option === "remove_watch_status") {
        editWatchStatus("remove_watch_status", media_type, media_id);
    } else if (watchlist_option === "plan_to_watch") {
        editWatchStatus("plan_to_watch", media_type, media_id);
    } else if (watchlist_option === "completed") {
        editWatchStatus("finished_watching", media_type, media_id);
    }
}

// CSRF token required to pass from javascript for POST via this function
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function addReview(media_type, media_id){
    const review = document.getElementById('review_textarea').value;
    const score = document.getElementById('review_score').value;
    const review_div = document.getElementById('viewEdit');
    fetch(`/review/${media_type}/${media_id}/`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            review: review,
            score: score
        })
    })
    .then (response => response.json())
    .then (response => {
        console.log(response.message);
        review_div.innerHTML = `<a href="" href="" data-toggle="modal" data-target="#editReviewModal">Your score: ${response.user_review_score}/10</a>`
    })
}

function showEditReview(score) {
    const show_edit_btn = document.getElementById("show_edit");
    const edit_btn = document.getElementById("editReviewBtn");
    const edit_review_score = document.getElementById("edit_review_score");
    const editReviewModalLabel = document.getElementById("editReviewModalLabel");
    const viewReviewModalLabel = document.getElementById("viewReviewModalLabel");
    const edit_review_textarea = document.getElementById("edit_review_textarea");
    show_edit_btn.setAttribute("hidden", true);
    viewReviewModalLabel.setAttribute("hidden", true);
    edit_btn.hidden = false;
    edit_review_score.hidden = false;
    editReviewModalLabel.hidden = false;
    edit_review_textarea.readOnly = false;
    edit_review_score.value = `${score}`;
}

function resetEditReview() {
    const show_edit_btn = document.getElementById("show_edit");
    const edit_btn = document.getElementById("editReviewBtn");
    const edit_review_score = document.getElementById("edit_review_score");
    const editReviewModalLabel = document.getElementById("editReviewModalLabel");
    const viewReviewModalLabel = document.getElementById("viewReviewModalLabel");
    const edit_review_textarea = document.getElementById("edit_review_textarea");
    show_edit_btn.hidden = false;
    viewReviewModalLabel.hidden = false;
    edit_btn.hidden = true;
    edit_review_score.hidden = true;
    editReviewModalLabel.hidden = true;
    edit_review_textarea.readOnly = true;
}

// This function seems to only work one time
function editReview(media_type, media_id) {
    const review = document.getElementById('edit_review_textarea').value;
    const score = document.getElementById('edit_review_score').value;
    const review_div = document.getElementById('viewEdit');
    const show_edit = document.getElementById("show_edit");
    const average_review_score = document.getElementById("average_score");
    fetch(`/editReview/${media_type}/${media_id}/`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            review: review,
            score: score
        })
    })
    .then (response => response.json())
    .then (response => {
        console.log(response.average_score);
        review_div.innerHTML = `Your score: ${response.user_review_score}/10`;
        average_review_score.innerHTML = `Average Score: ${response.average_score}`;
        
        resetEditReview();
    })
}

function searchHTMLInfiniteScroll() {
    console.log("scroll");
}

if (window.location.pathname=='/query/') {
    document.addEventListener('DOMContentLoaded',() => {
        const total_pages = parseInt(document.getElementById("total_pages").innerHTML);
        const search_query = document.getElementById("search_query").innerHTML;
        const search_container = document.getElementById("search_container");
        var page_number = 2;
        window.onscroll = () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight && total_pages > 1 && page_number <= total_pages) {
            const options = {
            method: 'GET',
            headers: {
                accept: 'application/json',
                Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3OTkyNTg5MzI4ZjA4MTJlYzM2ZTJmZjk0MTYwNmUxYiIsInN1YiI6IjY0N2MxZGE1OTM4MjhlMDBiZjllYjkxNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2gDv5tzYMOJOHdNwEqfr7vvWU-zbALQfys14gyWt0pE'
            }
            };
            fetch(`https://api.themoviedb.org/3/search/multi?query=${search_query}&include_adult=false&language=en-US&page=${page_number}`,options)
            .then (response => response.json())
            .then (response => {
                console.log(response);
                filterSearch(response.results);
            })
            .catch(err => console.error(err));
            page_number += 1;
        }
    };
})}

function filterSearch(response) {
    for (const result of response) {
        if (result.media_type != 'person' && result.media_type != 'collection') {
            console.log(result.poster_path);
            const newDiv = document.createElement("div");
            const backdrop_url = "https://www.themoviedb.org/t/p/w440_and_h660_face";
            var empty_poster_url = "https://cdn.vectorstock.com/i/preview-1x/48/06/image-preview-icon-picture-placeholder-vector-31284806.jpg";
            newDiv.classList.add("search_results_div")
            if (result.poster_path != null || result.poster_path) {
                var poster_path = `${backdrop_url}${result.poster_path}`;
            } else {
                var poster_path = `${empty_poster_url}`;
            }
            
            if (result.media_type === 'tv') {
                newDiv.innerHTML = `
                        <a href="/media/${result.media_type}/${result.id}/" class="a_results">
                            <div class="search_results_title">
                                ${result.name}
                            </div>
                            <div class="search_results_poster">
                                <img src="${poster_path}">
                            </div>
                        </a>
                `
            } else {
                newDiv.innerHTML = `
                        <a href="/media/${result.media_type}/${result.id}/" class="a_results">
                            <div class="search_results_title">
                                ${result.title}
                            </div>
                            <div class="search_results_poster">
                                <img src="${poster_path}">
                            </div>
                        </a>
                `
            }
            if (result.poster_path = "") {
                
            }
            document.getElementById("search_container").appendChild(newDiv);
        }
    }
}

function showMovieReviewTab() {
    const movie_review_divs = document.getElementById("movie_review_tab");
    const tv_review_divs = document.getElementById("tv_review_tab");
    const movie_modal_tab = document.getElementById("movie_modal_tab");
    const tv_modal_tab = document.getElementById("tv_modal_tab");
    movie_review_divs.hidden = false;
    tv_review_divs.hidden = true;
    movie_modal_tab.classList.add("active");
    tv_modal_tab.classList.remove("active");

}

function showTvReviewTab() {
    const movie_review_divs = document.getElementById("movie_review_tab");
    const tv_review_divs = document.getElementById("tv_review_tab");
    const movie_modal_tab = document.getElementById("movie_modal_tab");
    const tv_modal_tab = document.getElementById("tv_modal_tab");
    tv_review_divs.hidden = false;
    movie_review_divs.hidden = true;
    tv_modal_tab.classList.add("active");
    movie_modal_tab.classList.remove("active");
}

if (window.location.pathname.indexOf('/movie_user_watchlist/') === 0) {
    document.addEventListener("DOMContentLoaded", () =>  {
    const movie_watching_tab = document.getElementById("movie_watching_tab");
    const movie_planned_tab = document.getElementById("movies_planned_tab");
    const movie_completed_tab = document.getElementById("movie_completed_tab");
    const watching_div = document.getElementById("watching_div");
    const planned_div = document.getElementById("planned_div");
    const completed_div = document.getElementById("completed_div");
    movie_watching_tab.onclick = () => {
        watching_div.hidden = false;
        movie_watching_tab.classList.add("active");
        movie_watching_tab.style.color = "black";
        planned_div.hidden = true;
        movie_planned_tab.classList.remove("active");
        movie_planned_tab.style.color = "white";
        completed_div.hidden = true;
        movie_completed_tab.classList.remove("active");
        movie_completed_tab.style.color = "white";

    }
    movie_planned_tab.onclick = () => {
        watching_div.hidden = true;
        movie_watching_tab.classList.remove("active")
        movie_watching_tab.style.color = "white";
        planned_div.hidden = false;
        movie_planned_tab.classList.add("active");
        movie_planned_tab.style.color = "black";
        completed_div.hidden = true;
        movie_completed_tab.classList.remove("active");
        movie_completed_tab.style.color = "white";
    }
    movie_completed_tab.onclick = () => {
        watching_div.hidden = true;
        movie_watching_tab.classList.remove("active");
        movie_watching_tab.style.color = "white";
        planned_div.hidden = true;
        movie_planned_tab.classList.remove("active");
        movie_planned_tab.style.color = "white";
        completed_div.hidden = false;
        movie_completed_tab.classList.add("active");
        movie_completed_tab.style.color = "black";
    }
    
    const watchlist_score = document.getElementsByClassName("watchlist_score");
    for (var i = 0; i < watchlist_score.length; i++) {
        if (watchlist_score[i].innerHTML.trim() == "") {
            watchlist_score[i].innerHTML = "-/10";
        }
    }
    })
}

if (window.location.pathname.indexOf('/tv_user_watchlist/') === 0) {
    document.addEventListener("DOMContentLoaded", () =>  {
    const tv_watching_tab = document.getElementById("tv_watching_tab");
    const tv_planned_tab = document.getElementById("tv_planned_tab");
    const tv_completed_tab = document.getElementById("tv_completed_tab");
    const watching_div = document.getElementById("watching_div");
    const planned_div = document.getElementById("planned_div");
    const completed_div = document.getElementById("completed_div");
    tv_watching_tab.onclick = () => {
        watching_div.hidden = false;
        tv_watching_tab.classList.add("active");
        tv_watching_tab.style.color = "black";
        planned_div.hidden = true;
        tv_planned_tab.classList.remove("active");
        tv_planned_tab.style.color = "white";
        completed_div.hidden = true;
        tv_completed_tab.classList.remove("active");
        tv_completed_tab.style.color = "white";

    }
    tv_planned_tab.onclick = () => {
        watching_div.hidden = true;
        tv_watching_tab.classList.remove("active")
        tv_watching_tab.style.color = "white";
        planned_div.hidden = false;
        tv_planned_tab.classList.add("active");
        tv_planned_tab.style.color = "black";
        completed_div.hidden = true;
        tv_completed_tab.classList.remove("active");
        tv_completed_tab.style.color = "white";
    }
    tv_completed_tab.onclick = () => {
        watching_div.hidden = true;
        tv_watching_tab.classList.remove("active");
        tv_watching_tab.style.color = "white";
        planned_div.hidden = true;
        tv_planned_tab.classList.remove("active");
        tv_planned_tab.style.color = "white";
        completed_div.hidden = false;
        tv_completed_tab.classList.add("active");
        tv_completed_tab.style.color = "black";
    }

    const watchlist_score = document.getElementsByClassName("watchlist_score");
    for (var i = 0; i < watchlist_score.length; i++) {
        if (watchlist_score[i].innerHTML.trim() == "") {
            watchlist_score[i].innerHTML = "-/10";
        }
    }
    })
}