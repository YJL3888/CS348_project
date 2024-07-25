import type { RequestHandler } from "@sveltejs/kit";
import { PUBLIC_BACKEND_BASE } from "$env/static/public";

export const POST: RequestHandler = async ({ fetch, request, cookies }) => {
    return fetch(PUBLIC_BACKEND_BASE + "/favorites/toggle", {
        body: await request.text(),
        method: request.method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${cookies.get('token')}`
        }
    });
};
