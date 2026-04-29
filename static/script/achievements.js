async function copyDiv() {
    const response = await fetch("/view_your_achievements");
    const data = await response.json();

    const container = document.getElementById("container");
    const template = container.querySelector(".item");

    data.forEach(item => {
        const clone = template.cloneNode(true);
        clone.querySelector("header .name_event").textContent = item.event_id;
        clone.querySelector("header .category").textContent = item.category;
        clone.querySelector("main .document_url").href = item.document_url;
        clone.querySelector("main .document_url .result").textContent = item.result;
        clone.querySelector("footer .created_at").textContent = item.created_at;

        container.appendChild(clone);
    });
    // template.remove();
}

copyDiv();

document.querySelector(".add_achievements").addEventListener("click", ()=>{
    window.location.href = "/add_achievements";
});
