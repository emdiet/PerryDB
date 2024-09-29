// Subject, Observable, Observer

export type Observer<T> = {
    next: (value: T) => void;
    error: (error: any) => void;
    complete: () => void;
};

export type SimpleObserver<T> = (value: T) => void; 

export type Subscription = {
    unsubscribe: () => void;
};

type _Subject<T> = Observable<T> & {
    next: (value: T) => void;
    error: (error: any) => void;
    complete: () => void;
}

export type Observable<T> = {
    subscribe: (observer: Observer<T>) => Subscription;
    pipe: <U>(fn: (value: T) => U) => Observable<U>;
};

export class Subject<T> {
    private observers: {key: symbol, observer: Observer<T>}[] = [];
    private completed = false;

    constructor() {
        this.observers = [];
    }

    next(value: T) {
        if (this.completed) {
            console.warn('REACTIVE: Attempted to emit value on a completed Subject');
            return;
        }
        this.observers.forEach(({observer}) => observer.next(value));
    }

    error(error: any) {
        this.observers.forEach(({observer}) => observer.error(error));
    }

    complete() {
        this.observers.forEach(({observer}) => observer.complete());
        this.completed = true;
        this.observers = [];

    }

    subscribe(observer: Observer<T>): Subscription {
        const key = Symbol();
        this.observers.push({key, observer});
        return {
            unsubscribe: () => {
                this.observers = this.observers.filter(({key: _key}) => _key !== key);
            }
        };
    }

    pipe<U>(fn: (value: T) => U): Observable<U> {
        const subject = new Subject<U>();
        this.subscribe({
            next: (value) => subject.next(fn(value)),
            error: (error) => subject.error(error),
            complete: () => subject.complete()
        });
        return subject;
    }

    asObservable(): Observable<T> {
        return this;
    }
}