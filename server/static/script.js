async function addUser() {
    const name = document.getElementById("nameInput").value;
    if (!name) {
        Toastify({
            text: "Введите имя!",
            duration: 3000,
        }).showToast();
        return;
    }

    const response = await fetch("/add_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });

    const result = await response.json();
    Toastify({
        text: result.message,
        duration: 3000,
    }).showToast();

    console.log(result.message);

    getUsers();
}

async function getUsers() {
    const response = await fetch("/get_users");
    const users = await response.json();

    const userList = document.getElementById("userList");
    userList.innerHTML = ""; // Очищаем список

    users.forEach(user => {
        const li = document.createElement("li");
        li.textContent = `${user.id}: ${user.name}`;

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Удалить";
        deleteButton.onclick = () => deleteUser(user.id);

        li.appendChild(deleteButton);
        userList.appendChild(li);
    });
}

async function deleteUser(userId) {
    const response = await fetch("/delete_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: userId })
    });

    const result = await response.json();
    Toastify({
        text: result.message,
        duration: 3000,
    }).showToast();

    console.log(result.message);

    getUsers(); // Обновляем список
}
