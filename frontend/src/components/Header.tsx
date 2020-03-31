import * as React from 'react'
import * as ReactDOM from 'react-dom'
import 'font-awesome/css/font-awesome.min.css'
import './Header.css'

export default function Header(): JSX.Element{
    return(
        <div>
        <nav className="navbar">
            <ul className="navbar-nav">
                <li className="logo">
                    <a href="#" className="nav-link">
                        <span className="link-text">Liran</span>
                        <i className="fa fa-size fa-barcode"></i>
                    </a>
                </li>
                <li className="nav-item">
                    <a href="#" className="nav-link">
                        <i className="fa fa-size fa-search"></i>
                        <span className="link-text">Search</span>
                    </a>
                </li>
                <li className="nav-item">
                    <a href="#" className="nav-link">
                        <i className="fa fa-fire fa-size"></i>
                        <span className="link-text">Hot</span>
                    </a>
                </li>
                <li className="nav-item">
                    <a href="#" className="nav-link">
                        <i className="fa fa-android fa-size"></i>
                        <span className="link-text">Tech</span>
                    </a>
                </li>
                <li className="nav-item">
                    <a href="#" className="nav-link">
                        <i className="fa fa-sign-out fa-size"></i>
                        <span className="link-text">Exit</span>
                    </a>
                </li>
            </ul>
        </nav>
        <main>
            <h1>PEShop Design Try 1</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis in urna vulputate, fermentum est at, rutrum augue. Praesent convallis nec augue et sagittis. Aenean vitae bibendum tortor. Nullam euismod molestie ante a euismod. Integer fringilla sem arcu, mattis eleifend turpis faucibus sit amet. Phasellus sit amet velit vitae est interdum feugiat et non erat. Aliquam ultricies massa a mauris malesuada gravida. Pellentesque faucibus nec odio id ultricies. Sed pretium augue et orci dignissim, feugiat blandit nibh blandit. Vivamus ut leo ut felis mollis venenatis quis vitae nibh. Maecenas sit amet viverra est. Pellentesque ac egestas orci, sed consequat ante. Morbi varius, lacus sed pulvinar semper, lectus purus dapibus sapien, id fringilla urna nisl eget nisl.

                Suspendisse pharetra quam sit amet nunc volutpat, eget interdum justo fringilla. Suspendisse libero mi, sagittis vel libero vel, sagittis mollis sem. Cras tincidunt pretium orci vitae fringilla. Nullam vel nunc eu dolor bibendum rhoncus eget nec lectus. Mauris imperdiet ligula sit amet porttitor vestibulum. Proin at urna non turpis posuere interdum vitae nec enim. Aenean laoreet posuere vestibulum. Vestibulum nec rutrum justo. Nunc ac vestibulum nulla, in facilisis ante. Aliquam semper felis velit, nec venenatis risus interdum vitae. Donec quam mi, eleifend volutpat sapien vel, aliquet efficitur lacus. Integer ut semper erat. Etiam non mauris ut turpis efficitur semper. Sed purus est, semper ac ligula eget, eleifend tincidunt est. Donec dignissim sem purus, a fermentum neque tempor sed.

                Fusce quis leo id justo tincidunt pretium sit amet et diam. Aliquam erat volutpat. Nullam velit ante, aliquet sit amet nunc eu, blandit finibus leo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aliquam egestas odio vitae aliquet consequat. Donec efficitur tincidunt iaculis. Quisque rutrum nunc nec massa faucibus suscipit. In sed venenatis augue. Donec mi nisi, rhoncus in elit hendrerit, facilisis vulputate felis. Nam gravida, nunc eu scelerisque ultrices, enim diam tempus lorem, quis accumsan libero lorem ac ipsum. Nunc hendrerit augue ut purus faucibus maximus. Suspendisse ipsum velit, eleifend et feugiat sit amet, pharetra elementum tortor. Curabitur quam sem, mollis sed elit sit amet, rhoncus lobortis dui. Maecenas gravida rhoncus libero quis finibus. Sed quam magna, tincidunt sit amet justo eget, facilisis consequat purus. Sed laoreet diam ut neque pellentesque vestibulum.

                Donec vel sapien sed diam interdum ultrices. In hac habitasse platea dictumst. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vivamus non aliquam lectus, luctus tristique risus. Fusce aliquet, arcu sed egestas faucibus, tellus velit scelerisque eros, sed pulvinar magna erat ac ante. Ut mattis neque at ipsum malesuada tincidunt. Quisque dolor libero, faucibus eget auctor sit amet, vestibulum pretium arcu. Donec ac arcu nec leo aliquam feugiat. Donec sagittis, lectus eu egestas dapibus, purus ex imperdiet dui, finibus gravida massa neque et lorem. Nullam auctor sem sed ante aliquet rutrum. Sed varius ante quis purus vestibulum, et tincidunt neque hendrerit. Ut hendrerit mauris dui, sit amet rutrum ligula fringilla id. Etiam aliquam tincidunt libero, venenatis semper nisi semper nec. Fusce tristique, tortor at ultrices molestie, massa urna consequat ligula, quis lacinia lorem ante eu turpis.

                Quisque lobortis sollicitudin tellus. Praesent imperdiet nisl turpis, eu mattis erat condimentum at. Aliquam pharetra, urna vitae consectetur interdum, enim lacus porta magna, at fringilla est turpis non libero. Maecenas facilisis tincidunt metus, sit amet suscipit urna. Mauris blandit sagittis aliquam. Suspendisse quis mi lobortis, dignissim elit sed, ultrices urna. Proin vitae leo consequat, commodo odio posuere, tristique felis. Donec mattis convallis enim vel aliquam. Mauris viverra elit eu ullamcorper iaculis. Ut odio urna, facilisis vel volutpat vitae, sollicitudin placerat lacus.
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis in urna vulputate, fermentum est at, rutrum augue. Praesent convallis nec augue et sagittis. Aenean vitae bibendum tortor. Nullam euismod molestie ante a euismod. Integer fringilla sem arcu, mattis eleifend turpis faucibus sit amet. Phasellus sit amet velit vitae est interdum feugiat et non erat. Aliquam ultricies massa a mauris malesuada gravida. Pellentesque faucibus nec odio id ultricies. Sed pretium augue et orci dignissim, feugiat blandit nibh blandit. Vivamus ut leo ut felis mollis venenatis quis vitae nibh. Maecenas sit amet viverra est. Pellentesque ac egestas orci, sed consequat ante. Morbi varius, lacus sed pulvinar semper, lectus purus dapibus sapien, id fringilla urna nisl eget nisl.

                Suspendisse pharetra quam sit amet nunc volutpat, eget interdum justo fringilla. Suspendisse libero mi, sagittis vel libero vel, sagittis mollis sem. Cras tincidunt pretium orci vitae fringilla. Nullam vel nunc eu dolor bibendum rhoncus eget nec lectus. Mauris imperdiet ligula sit amet porttitor vestibulum. Proin at urna non turpis posuere interdum vitae nec enim. Aenean laoreet posuere vestibulum. Vestibulum nec rutrum justo. Nunc ac vestibulum nulla, in facilisis ante. Aliquam semper felis velit, nec venenatis risus interdum vitae. Donec quam mi, eleifend volutpat sapien vel, aliquet efficitur lacus. Integer ut semper erat. Etiam non mauris ut turpis efficitur semper. Sed purus est, semper ac ligula eget, eleifend tincidunt est. Donec dignissim sem purus, a fermentum neque tempor sed.

                Fusce quis leo id justo tincidunt pretium sit amet et diam. Aliquam erat volutpat. Nullam velit ante, aliquet sit amet nunc eu, blandit finibus leo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aliquam egestas odio vitae aliquet consequat. Donec efficitur tincidunt iaculis. Quisque rutrum nunc nec massa faucibus suscipit. In sed venenatis augue. Donec mi nisi, rhoncus in elit hendrerit, facilisis vulputate felis. Nam gravida, nunc eu scelerisque ultrices, enim diam tempus lorem, quis accumsan libero lorem ac ipsum. Nunc hendrerit augue ut purus faucibus maximus. Suspendisse ipsum velit, eleifend et feugiat sit amet, pharetra elementum tortor. Curabitur quam sem, mollis sed elit sit amet, rhoncus lobortis dui. Maecenas gravida rhoncus libero quis finibus. Sed quam magna, tincidunt sit amet justo eget, facilisis consequat purus. Sed laoreet diam ut neque pellentesque vestibulum.

                Donec vel sapien sed diam interdum ultrices. In hac habitasse platea dictumst. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vivamus non aliquam lectus, luctus tristique risus. Fusce aliquet, arcu sed egestas faucibus, tellus velit scelerisque eros, sed pulvinar magna erat ac ante. Ut mattis neque at ipsum malesuada tincidunt. Quisque dolor libero, faucibus eget auctor sit amet, vestibulum pretium arcu. Donec ac arcu nec leo aliquam feugiat. Donec sagittis, lectus eu egestas dapibus, purus ex imperdiet dui, finibus gravida massa neque et lorem. Nullam auctor sem sed ante aliquet rutrum. Sed varius ante quis purus vestibulum, et tincidunt neque hendrerit. Ut hendrerit mauris dui, sit amet rutrum ligula fringilla id. Etiam aliquam tincidunt libero, venenatis semper nisi semper nec. Fusce tristique, tortor at ultrices molestie, massa urna consequat ligula, quis lacinia lorem ante eu turpis.

                Quisque lobortis sollicitudin tellus. Praesent imperdiet nisl turpis, eu mattis erat condimentum at. Aliquam pharetra, urna vitae consectetur interdum, enim lacus porta magna, at fringilla est turpis non libero. Maecenas facilisis tincidunt metus, sit amet suscipit urna. Mauris blandit sagittis aliquam. Suspendisse quis mi lobortis, dignissim elit sed, ultrices urna. Proin vitae leo consequat, commodo odio posuere, tristique felis. Donec mattis convallis enim vel aliquam. Mauris viverra elit eu ullamcorper iaculis. Ut odio urna, facilisis vel volutpat vitae, sollicitudin placerat lacus.</p>
        </main>
        </div>

    )
}
