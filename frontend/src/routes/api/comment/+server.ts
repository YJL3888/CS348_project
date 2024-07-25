import type { RequestHandler } from "./$types";
import { PUBLIC_BACKEND_BASE } from "$env/static/public";

export const POST: RequestHandler = async ({ fetch, request, cookies }) => {
    return await fetch(PUBLIC_BACKEND_BASE + "/restaurants/comment", {
        method: 'POST',
        body: await request.formData(),
        headers: {
            Authorization: 'Bearer ' + cookies.get('token')
        }
    });
};
