document.addEventListener("DOMContentLoaded", () => {
    loadGroups();
});

function getCSRFToken() {
    let csrfInput = document.querySelector("input[name='csrf_token']");
    return csrfInput ? csrfInput.value : "";
}

function loadGroups() {
    fetch('/get_groups')
        .then(response => response.json())
        .then(data => {
            let groupSelect = document.getElementById('group');
            groupSelect.innerHTML = '<option value="">Выберите группу</option>';
            data.groups.forEach(group => {
                let option = document.createElement('option');
                option.value = group.id;
                option.textContent = group.name;
                groupSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Ошибка загрузки групп:", error));
}

function loadStudents(groupId) {
    if (!groupId) return;

    fetch(`/get_students?group_id=${groupId}`)
        .then(response => response.json())
        .then(data => {
            let studentSelect = document.getElementById('student');
            studentSelect.innerHTML = '<option value="">Выберите студента</option>';
            data.students.forEach(student => {
                let option = document.createElement('option');
                option.value = student.id;
                option.textContent = `${student.last_name} ${student.first_name}`;
                studentSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Ошибка загрузки студентов:", error));
}

function setCookie(name, value, seconds) {
    let date = new Date();
    date.setTime(date.getTime() + (seconds * 1000));
    document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/`;
}

function checkLocation() {
    if (document.cookie.includes("attendance")) {
        alert("Вы уже отметились! Повторная отметка невозможна.");
        return;
    }

    const groupId = document.getElementById('group').value;
    const studentId = document.getElementById('student').value;

    if (!groupId || !studentId) {
        alert('Выберите группу и студента!');
        return;
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            let csrfToken = getCSRFToken(); // Получаем CSRF токен

            fetch('/check_location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken  // Передаём CSRF токен в заголовке
                },
                body: JSON.stringify({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    student_id: studentId,
                    group_id: groupId
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerText = `${data.result}`;

                setCookie("attendance", "marked", 5400);
            })
            .catch(error => console.error("Ошибка при запросе:", error));
        }, function(error) {
            console.error("Ошибка геолокации:", error);
        });
    } else {
        alert('Геолокация не поддерживается в вашем браузере');
    }
}
