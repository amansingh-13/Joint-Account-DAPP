pragma solidity ^0.4.24;

contract Queue {
    mapping(uint256 => uint) queue;
    uint256 first = 1;
    uint256 last = 0;

    function enqueue(uint data) public {
        last += 1;
        queue[last] = data;
    }

    function dequeue() public returns (uint data) {
        require(last >= first); 

        data = queue[first];

        delete queue[first];
        first += 1;
    }
    
    function empty () 
    view 
    public
    returns (bool)
    {
        if (last<first) {
            return true;
        }
        return false;
    }
}

contract Dapp{

    uint256 MAX_INT = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
    uint numUser;
    struct User {
        uint user_id;
        string user_name;
        uint is_active;
    }
    mapping(uint=>User) available_users;
    // mapping(address=>bbol) used_address;
    
    
    struct Edge{
        uint user_id;
        uint val;
    }
    
    // struct Queue {
    //     mapping(uint=>uint) data;
    //     uint first;
    //     uint last;
    // }
    
    mapping(uint=>uint[]) peers;
    mapping(uint=>mapping(uint=>uint)) edges;


    constructor()public
    {
        numUser=0;
    }
    
    
    
    function registerUser(uint uid, string name)
    public 
    userNotPresent(uid)
    returns (bool)
    {
        // User storage u;
        // u.user_id=uid;
        // u.user_name=name;
        // u.is_active=true;
        available_users[uid]=User(uid,name,11);
        numUser++;
        return true;
    }
    
    function createAcc(uint uid1, uint uid2, uint val1, uint val2)
    public
    userPresent(uid1)
    userPresent(uid2)
    edgeNotAlreadyExist(uid1,uid2)
    returns (bool)
    {
        peers[uid1].push(uid2);
        peers[uid2].push(uid1);
        edges[uid1][uid2]=val1;
        edges[uid2][uid1]=val2;
        return true;
    }

    function closeAccount(uint uid1, uint uid2)
    public
    userPresent(uid1)
    userPresent(uid2)
    returns(bool)
    {
        uint idx=peers[uid1].length+10;
        for (uint i=0; i<peers[uid1].length; i++){
            if (peers[uid1][i]==uid2){
                idx=i;
                break;
            }
        }
        if (idx>=peers[uid1].length) return false;
        for (i=idx; i<peers[uid1].length-1; i++){
            peers[uid1][i]=peers[uid1][i+1];
        }
        delete peers[uid1][peers[uid1].length-1];
        peers[uid1].length--;
        idx=peers[uid2].length+10;

        for (i=0; i<peers[uid2].length; i++){
            if (peers[uid2][i]==uid1){
                idx=i;
                break;
            }
        }
        if (idx>=peers[uid2].length) return false;

        for (i=idx; i<peers[uid2].length-1; i++){
            peers[uid2][i]=peers[uid2][i+1];
        }
        delete peers[uid2][peers[uid2].length-1];
        peers[uid2].length--;
        
        delete edges[uid1][uid2];
        delete edges[uid2][uid1];
        
        return true;
    }
    
   
    
    // function enqueue(Queue q, uint a) 
    // private 
    // returns (Queue)
    // {
    //     q.last+=1;
    //     q.data[q.last]=a;
    //     return q;
    // }
    
    // function dequeu(Queue q)
    // private 
    // returns (uint, Queue)
    // {
    //     require(q.last>=q.first);
    //     uint val=q.data[q.first];
    //     delete q.data[q.first];
        
    //     return (val, q);
    // }
    
    // function empty (Queue q)
    // private 
    // returns (bool)
    // {
    //     if (q.last<q.first){
    //         return true;
    //     }
    //     return false;
    // }
    
    // struct Helper {
    //     mapping(uint=>bool) visited;
    //     mapping(uint=>uint) dist;
    //     mapping(uint=>int) pred;
    // }
    function findShortestPath(uint start, uint end, uint minVal)
    private
    returns (bool,uint [])
    {
        // uint n=numUser;
        // bool[] storage visited;
        // uint[] storage dist;
        int[] storage pred;
        // Helper memory h;
        Queue q=new Queue();
        // q.first=1;
        // q.last=0;
        
        for (uint i=0; i<numUser; i++){
            // h.visited[i]=false;
            // h.dist[i]=MAX_INT;
            pred[i]=-1;
        }
        // h.visited[start]=true;
        // h.dist[start]=0;
        pred[start]=int(start);
        q.enqueue(start);
        bool check=false;
        while (!q.empty()){    
            uint u;
            u=q.dequeue();
            for (i=0; i<peers[u].length; i++){
                uint cn=peers[u][i];
                uint value=edges[u][cn];
                
                if (pred[cn]==-1 && value>minVal){
                    // h.visited[cn]=true;
                    // h.dist[cn]=h.dist[cn]+1;
                    pred[cn]=int(u);
                    q.enqueue(cn);
                    
                    if (cn==end){
                        check=true;
                        break;
                    }
                }
            }
        }
        
        uint[] storage path;
        if (check==false){
            return (check, path);
        }
        
        int crw=int(end);
        
        while (crw!=int(start)){
            path.push(uint(crw));
            crw=pred[uint(crw)];
        }
        path.push(start);
        return (check, path);
        
        
    }
    
    
    function sendAmount(uint uid1, uint uid2, uint val)
    public
    userPresent(uid1)
    userPresent(uid2)
    returns (bool)
    {
        bool check;
        uint[] memory path; 
        (check,path)=findShortestPath(uid1, uid2, val);
        return true;
        if (check==false){
            return false;
        }
        for (uint i=path.length-1; i>0; i--){
            edges[path[i]][path[i-1]]-=val;
            edges[path[i-1]][path[i]]+=val;
        }
        return true;
        
    }




    
    
    modifier userPresent(uint id){
        require(available_users[id].is_active==11);
        _;
    }
    
    modifier userNotPresent(uint id){
        require(available_users[id].is_active!=11);
        _;
        
    }
    // modifier notRegisteredOnce(address adr){
    //     require(~used_address[adr]);
    //     _;
    // }
    // modifier legalAccess(address adr, uint uid){
    //     require(available_users[uid].addr=adr);
    //     _;
    // }
    modifier edgeNotAlreadyExist(uint uid1, uint uid2){
        bool check=false;
        for (uint i=0; i<peers[uid1].length;i++){
            if (peers[uid1][i]==uid2){
                check=true;
                break;
            }
        }
        require(check==false);
        _;
    }
    modifier edgeAlreadyExist(uint uid1, uint uid2){
        bool check=false;
        for (uint i=0; i<peers[uid1].length;i++){
            if (peers[uid1][i]==uid2){
                check=true;
                break;
            }
        }
        require(check==true);
        _;
    }
    
    
}