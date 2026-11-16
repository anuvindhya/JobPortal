
document.addEventListener("DOMContentLoaded", function () {

    // Delete confirmation

    const deleteForms = document.querySelectorAll(
        "form[data-confirm]"
    );

    deleteForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const message = form.getAttribute("data-confirm");

            const result = confirm(message);

            if (!result) {
                event.preventDefault();
            }

        });

    });


    // Bootstrap form validation

    const forms = document.querySelectorAll(".needs-validation");

    forms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            if (!form.checkValidity()) {

                event.preventDefault();
                event.stopPropagation();

            }

            form.classList.add("was-validated");

        });

    });

});
