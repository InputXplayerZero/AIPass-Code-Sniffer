/**
 * Simple test TypeScript file for code sniffer testing.
 */

interface User {
    name: string;
    age: number;
}

export class UserManager {
    private users: User[] = [];

    /**
     * Add a new user to the system
     */
    addUser(user: User): void {
        this.users.push(user);
    }

    /**
     * Get user by name
     */
    getUserByName(name: string): User | undefined {
        return this.users.find(user => user.name === name);
    }

    /**
     * Get all users
     */
    getAllUsers(): User[] {
        return [...this.users];
    }
}

export function createUser(name: string, age: number): User {
    return { name, age };
}

export default UserManager;
