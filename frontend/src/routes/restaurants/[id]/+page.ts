import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';
import { PUBLIC_BACKEND_BASE } from "$env/static/public";

export const load: PageLoad = async ({ params }) => {
    const res = await fetch(PUBLIC_BACKEND_BASE + '/restaurants/' + params.id);
    if (!res.ok) error(res.status, res.statusText);
    return {restaurant: await res.json()};
};
