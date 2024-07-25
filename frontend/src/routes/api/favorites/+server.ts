import type { RequestHandler } from "@sveltejs/kit";
import { PUBLIC_BACKEND_BASE } from "$env/static/public";

export const GET: RequestHandler = async ({ fetch, cookies }) => {
    return fetch(PUBLIC_BACKEND_BASE + "/favorites", {
        headers: {
            'Authorization': `Bearer ${cookies.get('token')}`
        }
    });
};
