// Subject, Observable, Observer
export class Subject {
    constructor() {
        this.observers = [];
        this.completed = false;
        this.observers = [];
    }
    next(value) {
        if (this.completed) {
            console.warn('REACTIVE: Attempted to emit value on a completed Subject');
            return;
        }
        this.observers.forEach(({ observer }) => observer.next(value));
    }
    error(error) {
        this.observers.forEach(({ observer }) => observer.error(error));
    }
    complete() {
        this.observers.forEach(({ observer }) => observer.complete());
        this.completed = true;
        this.observers = [];
    }
    subscribe(observer) {
        const key = Symbol();
        this.observers.push({ key, observer });
        return {
            unsubscribe: () => {
                this.observers = this.observers.filter(({ key: _key }) => _key !== key);
            }
        };
    }
    pipe(fn) {
        const subject = new Subject();
        this.subscribe({
            next: (value) => subject.next(fn(value)),
            error: (error) => subject.error(error),
            complete: () => subject.complete()
        });
        return subject;
    }
    asObservable() {
        return this;
    }
}
//# sourceMappingURL=reactive.js.map