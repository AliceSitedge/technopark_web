'use strict';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrf_token = getCookie('csrftoken');

function vote(element) {
    let objectType;
    let objectId;
    if (element.getAttribute('data-qid') == null) {
        objectType = 'answer';
        objectId = element.getAttribute('data-aid');
    } else {
        objectType = 'question';
        objectId = element.getAttribute('data-qid');
    }

    let vote = element.getAttribute('data-vote');
    let data = {type: objectType, id: objectId, vote: vote};

    fetch(
        '/ask-alice/vote/', {
            method: 'POST',
            body: JSON.stringify(data),
            credentials: 'include',
            headers: {"X-CSRFToken": csrf_token},
        }
    )
        .then(response => response.json())
        .then(responseData => {
            let parent = element.parentNode;
            let textElement = parent.querySelector('div.text-center');

            textElement.textContent = responseData.rating;
        });

    return false;
}

function correct(element) {
    let answerId = element.getAttribute('data-aid');
    let action = element.getAttribute('data-action');
    let data = {aid: answerId, action: action};

    fetch(
        '/ask-alice/correct/', {
            method: 'POST',
            body: JSON.stringify(data),
            credentials: 'include',
            headers: {"X-CSRFToken": csrf_token},
        }
    )
        .then(response => response.json())
        .then(responseData => {
            let parent = element.parentNode.parentNode.parentNode;

            let textElement = parent.querySelector('div > .correct');
            console.log(textElement);
            if (responseData.correct === true) {
                textElement.style.visibility = 'visible';
            } else {
                textElement.style.visibility = 'hidden';
            }
        });

    return false;
}
