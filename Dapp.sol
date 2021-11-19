pragma solidity ^0.8;


contract Dapp {
    //data structure to store user data
    struct User {
        uint user_id;
        string user_name;
        bool is_active;
        uint number;
    }
    event UserAdded(uint uid);

    uint numUser = 0; // number of users in network 
    uint check_alive=0;
    mapping(uint => User) available_users; // dictionary from user_id=> user_data 
    uint[] parent; // index by number, value is uid
    
    struct Edge {
        uint user_id;
        uint val;
    }
    
    mapping(uint => uint[]) peers;
    mapping(uint => mapping(uint => uint)) public edges; // debug public
    
    // dummy function to check if contract has been successfully deployed
    function alive()
    public 
    {
        check_alive=1;
    }
    //registering new user 
    function registerUser(uint uid, string memory username)
    public 
    userNotPresent(uid)
    {
        emit UserAdded(uid);
        available_users[uid] = User(uid, username, true, numUser);
        parent.push(0);
        numUser++;
    }
    
    //creating joint account of two user 
    function createAcc(uint uid1, uint uid2, uint val1, uint val2)
    public
    userPresent(uid1)
    userPresent(uid2)
    edgeNotAlreadyExist(uid1, uid2)
    
    {
        peers[uid1].push(uid2);
        peers[uid2].push(uid1);
        edges[uid1][uid2] = val1;
        edges[uid2][uid1] = val2;
    }

    // closing joint account of two user 
    function closeAccount(uint uid1, uint uid2)
    public
    userPresent(uid1)
    userPresent(uid2)
    edgeAlreadyExist(uid1, uid2)
    
    {
        uint idx;
        
        for (uint i=0; i<peers[uid1].length; i++){
            if (peers[uid1][i]==uid2){
                idx = i;
                break;
            }
        }
        for (uint i=idx; i<peers[uid1].length-1; i++){
            peers[uid1][i] = peers[uid1][i+1];
        }
        peers[uid1].pop();

        for (uint i=0; i<peers[uid2].length; i++){
            if (peers[uid2][i]==uid1){
                idx = i;
                break;
            }
        }
        for (uint i=idx; i<peers[uid2].length-1; i++){
            peers[uid2][i] = peers[uid2][i+1];
        }
        peers[uid2].pop();
        
        delete edges[uid1][uid2];
        delete edges[uid2][uid1];
        
    }

    // finding shortest path to send amount form one user to another
    function findShortestPath(uint start, uint end, uint minVal)
    private
    returns (bool)
    {
        Queue q = new Queue();
        
        for(uint i=0; i<numUser; i++){
            delete parent[i];
        }
        
        parent[available_users[start].number] = start;
        q.enqueue(start);
        bool found = false;
        while (!q.empty()){    
            uint u = q.dequeue();
            for (uint i=0; i<peers[u].length; i++){
                uint cn     = peers[u][i];
                uint value  = edges[u][cn];
                uint cn_num = available_users[cn].number;
                if (parent[cn_num]==0 && value>=minVal){
                    parent[cn_num] = u;
                    q.enqueue(cn);
                    if (cn==end){
                        found = true;
                        break;
                    }
                }
            }
            if(found)
                break;
        }
        
        return found;
    }
    
    // send amount from one user to another 
    function sendAmount(uint uid1, uint uid2, uint val)
    public
    userPresent(uid1)
    userPresent(uid2)
    
    {
        bool found = findShortestPath(uid1, uid2, val);
    
        if(!found){
            require(false, "No path found");
         
        }
        uint crw     = uid2;
        uint crw_num = available_users[uid2].number;
        while(crw != uid1){
            edges[crw][parent[crw_num]] += val;
            edges[parent[crw_num]][crw] -= val;
            crw     = parent[crw_num];
            crw_num = available_users[parent[crw_num]].number;
        }
        
    }

    // check if user_id alreay exist 
    modifier userPresent(uint id){
        assert(available_users[id].is_active);
        _;
    }
    //check if user_id is free
    modifier userNotPresent(uint id){
        assert(!available_users[id].is_active);
        _;
        
    }
    
    // check absence of joint account between two users 
    modifier edgeNotAlreadyExist(uint uid1, uint uid2){
        bool check = false;
        for (uint i=0; i<peers[uid1].length;i++){
            if (peers[uid1][i]==uid2){
                check = true;
                break;
            }
        }
        require(check==false);
        _;
    }

    // check presence of joint account between two users 
    modifier edgeAlreadyExist(uint uid1, uint uid2){
        bool check = false;
        for (uint i=0; i<peers[uid1].length;i++){
            if (peers[uid1][i]==uid2){
                check = true;
                break;
            }
        }
        require(check==true, "Joint account already exists");
        _;
    }
}

// Queue data structure, used to find shortes path between two nodes
contract Queue {
    mapping(uint256 => uint) queue;
    uint256 first = 1; 
    uint256 last  = 0;

    // add data to queue
    function enqueue(uint data) public 
    {
        last += 1;
        queue[last] = data;
    }

    //pop and return data from queue
    function dequeue() public returns (uint data)
    {
        require(last >= first);
        data = queue[first];
        delete queue[first];
        first += 1;
    }
    
    // check if queue is empty 
    function empty () view public returns (bool)
    {
        if (last < first) {
            return true;
        }
        return false;
    }
}
