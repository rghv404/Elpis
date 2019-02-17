const userInfoBox = document.getElementById('user-info-box');
const detailsBox = document.getElementsByClassName("details")[0];
const filePath = 'http://localhost:8001/get-cases';

let cases;

const onStart = () => {
    $.get(filePath, function (data) {
        console.log(data);
        cases = data;
        populateCase();
    })
};

const populateCase = () => {
    const caseBoxes = cases.map((first) => {
        const clone = detailsBox.cloneNode(true);
        const caseIdSpan = clone.getElementsByClassName('case-id')[0];
        const userNameSpan = clone.getElementsByClassName('user-name')[0];
        const userContactSpan = clone.getElementsByClassName('user-contact')[0];
        const userLocationSpan = clone.getElementsByClassName('user-location')[0];
        const causeSpan = clone.getElementsByClassName('cause')[0];
        const isTroll = clone.getElementsByClassName('troll-user')[0];
        const severitySpan = clone.getElementsByClassName('severity')[0];
        caseIdSpan.innerText = first.id[0];
        userNameSpan.innerText = first.name[0];
        userLocationSpan.innerText = first.location[0];
        severitySpan.innerText = first.severity_score[0];
        clone.style.display = "";
        userInfoBox.appendChild(clone);
        return clone;
    });
    console.log('Constructed case boxes', caseBoxes);
};
