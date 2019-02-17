const caseIdSpan = document.getElementById('case-id');
const userNameSpan = document.getElementById('user-name');
const userContactSpan = document.getElementById('user-contact');
const userLocationSpan = document.getElementById('user-location');
const causeSpan = document.getElementById('cause');
const isTroll = document.getElementById('troll-user');
const severitySpan = document.getElementById('severity');
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
    if (cases.length > 0) {
        const first = cases[0];
        caseIdSpan.innerText = first.id[0];
        userNameSpan.innerText = first.name[0];
        userLocationSpan.innerText = first.location[0];
        severitySpan.innerText = first.severity_score[0];
    }
};
