import type { Actions } from "./$types";
import { redirect } from "@sveltejs/kit";
import { PUBLIC_BACKEND_BASE } from "$env/static/public";

export const actions = {
    async default({ request, fetch, cookies }) {
        const res = await fetch(PUBLIC_BACKEND_BASE + "/login", {
            method: 'POST',
            body: new URLSearchParams(await request.formData())
        });
        let data;
        try {
            data = await res.json();
        } catch(e) {
            return { error: "An error occurred. Please try again later." };
        }
        console.log(data);
        if (res.ok && data.access_token) {
            cookies.set("token", data.access_token, {path: '/'});
            console.log('redirect');
            redirect(302, "/");
        }
        return data;
    }
} satisfies Actions;
