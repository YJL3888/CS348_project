import type { RequestHandler } from "./$types";
import { PUBLIC_BACKEND_BASE } from "$env/static/public";

export const POST: RequestHandler = async ({ fetch, request }) => {
    return await fetch(PUBLIC_BACKEND_BASE + "/password-reset", {
        method: 'POST',
        body: new URLSearchParams(await request.formData())
    });
};
