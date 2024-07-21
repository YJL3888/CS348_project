import type { RequestHandler } from "./$types";
import { BACKEND_BASE } from "$env/static/private";

export const POST: RequestHandler = async ({ fetch, request }) => {
    return fetch(BACKEND_BASE + "/password-reset/get-token", {
        method: 'POST',
        body: new URLSearchParams(await request.formData())
    });
};
