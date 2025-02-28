document.addEventListener("DOMContentLoaded", function () {
    const roleSelect = document.getElementById("role");
    const studentFields = document.getElementById("studentFields");  // ✅ Fixed ID
    const facultyFields = document.getElementById("facultyFields");  // ✅ Fixed ID
    const parentFields = document.getElementById("parentFields");  // ✅ Fixed ID

    function toggleFields() {
        studentFields.classList.toggle("d-none", roleSelect.value !== "Student");
        facultyFields.classList.toggle("d-none", roleSelect.value !== "Faculty");
        parentFields.classList.toggle("d-none", roleSelect.value !== "Parent");
    }

    roleSelect.addEventListener("change", toggleFields);
    toggleFields();  // Ensure correct fields show on page load
});
