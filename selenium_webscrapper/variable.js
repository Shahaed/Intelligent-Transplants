export class Variable {
    constructor(i, j, k) {
        this.i = i;
        this.j = j;
        this.k = k;
    }
    get loadi() {
        return this.i;
    };
    
    get loadj() {
        return this.j;
    };
    
    get loadk() {
        return this.k;
    };

};