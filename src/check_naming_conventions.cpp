#include <check_naming_conventions.hpp>
#include <string>
int main(int argc, char** argv){
        CheckNamingConventionsPolicy* cat = new CheckNamingConventionsPolicy();
        std::string buf = argv[1];
        srcSAXController control(buf);
        srcSAXEventDispatch::srcSAXEventDispatcher<> handler({cat}, false);
        control.parse(&handler); //Start parsing	
	return 0;
}