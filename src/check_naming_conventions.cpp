#include <check_naming_conventions.hpp>
int main(int argc, char** argv){
        CheckNamingConventionsPolicy* cat = new CheckNamingConventionsPolicy();
        srcSAXController control(argv[1]);
        srcSAXEventDispatch::srcSAXEventDispatcher<> handler({cat}, false);
        control.parse(&handler); //Start parsing	
	return 0;
}