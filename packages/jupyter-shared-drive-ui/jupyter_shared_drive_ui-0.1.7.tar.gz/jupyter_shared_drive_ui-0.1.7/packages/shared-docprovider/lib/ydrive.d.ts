import * as Y from 'yjs';
export declare class YDrive {
    constructor();
    get ydoc(): Y.Doc;
    private _newDir;
    isDir(path: string): boolean;
    get(path: string): Y.Map<any> | null;
    newUntitled(isDir: boolean, path?: string, ext?: string): string;
    createFile(path: string): void;
    createDirectory(path: string): void;
    delete(path: string): void;
    move(fromPath: string, toPath: string): void;
    private _ydoc;
    private _yroot;
}
