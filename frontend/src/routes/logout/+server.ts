import { redirect } from '@sveltejs/kit';

export function GET({ cookies }) {
	cookies.delete('token', { path: '/' });
	redirect(302, '/');
}
