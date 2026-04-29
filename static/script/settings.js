async function postTelegramData(data){
    console.log(data);
    if(data.error) return;
    
    const response = await fetch("/tg_auth", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({id_token: data.id_token}),
        credentials: "same-origin"
    });

    if (!response.ok) {
        const error = await response.json();
        console.log(error.detail);
    }
}