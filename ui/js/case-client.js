const mainSection = document.getElementById('main-background');
const userInfoBox = document.getElementsByClassName('user-info-box')[0];
//const detailsBox = document.getElementsByClassName("details")[0];
const detailsBox = userInfoBox;
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
        const pointsSpan = clone.getElementsByClassName('phq9-points')[0];
        caseIdSpan.innerText = first.id[0];
        userNameSpan.innerText = first.name[0];
        userLocationSpan.innerText = first.location[0];
        severitySpan.innerText = first.severity_score[0];
        pointsSpan.innerText = first.severity_score[0];
        userContactSpan.innerText = first.phone[0] || "Not known";
        clone.style.display = "";
        mainSection.appendChild(clone);
        return clone;
    });
    console.log('Constructed case boxes', caseBoxes);
};
