import type { RequestHandler } from "@sveltejs/kit";
import { PUBLIC_BACKEND_BASE } from "$env/static/public";

export const POST: RequestHandler = async ({ request, fetch, cookies }) => {
    return fetch(PUBLIC_BACKEND_BASE + "/favorites", {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${cookies.get('token')}`
        }
    });
};