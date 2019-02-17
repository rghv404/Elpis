const filePath = 'http://localhost:8001/get-cases';

const onStart = () => {
    $.get(filePath, function (data) {
        console.log(data);
    })
};
