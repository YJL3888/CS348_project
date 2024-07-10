import type { LayoutServerLoad } from './$types';
import { jwtDecode } from 'jwt-decode';

export const load: LayoutServerLoad = async ({ cookies }) => {
    const token = cookies.get('token');
    return {
        user: token ? jwtDecode(token) : null
    }
};
